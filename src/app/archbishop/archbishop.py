import logging

import requests
from flask import Blueprint, Response
from flask import request
from slack_sdk.errors import SlackApiError
from src.app.model.event.event import Event
from src.app.model.group.group import Group
from src.app.model.group.player import Player
from collections import namedtuple
from slack_bolt.adapter.flask import SlackRequestHandler


# Archbishop Logic
def construct_blueprint(bolt, config, messages, redis):
    archbishop = Blueprint('archbishop', __name__)
    log = logging.getLogger(__name__)
    handler = SlackRequestHandler(bolt)

    @archbishop.route("/")
    def hello():
        """ Test request (useful for spinning server up after inactivity) """
        return Response("Hello, World!", status=200)

    @archbishop.route("/scroll", methods=['POST'])
    def unroll():
        """ Handle slack command for scroll information """
        group = redis.get_complex(request.form["team_id"], Group)
        formatted_scroll = ""
        position = 0
        for record in group.scroll:
            position += 1
            formatted_scroll += messages.load_with_params(
                "command.scroll.entry",
                [str(position), record.name, str(record.streak), str(record.date)]
            )
        return Response(formatted_scroll, status=200)

    @archbishop.route("/group/<group_id>")
    def group(group_id):
        """ Get group information by id """
        log.debug(f"[get_group] Retrieving group for id [{group_id}]")
        return Response(str(redis.get_complex(group_id, Group)), status=200)

    @archbishop.route(config.EVENT_PATH, methods=['POST'])
    def event():
        """ Handle event request from Slack """
        log.debug(f"[event] New Event from Slack! [{str(request.get_json())}]")
        return handler.handle(request)

    @bolt.message(messages.load("event.message.keyword"))
    def handle_waffle(message, say):
        """ Receive and process new waffle score """
        log.debug("[handle_waffle] New Waffle Score received!")
        event = Event(message)
        group = get_group(event)
        player = get_player(event, group)

        log.debug(f"[handle_waffle] Updating player information for [{player.name}]")
        player.score += event.get_score()
        player.streak = event.get_streak()

        log.debug(f"[handle_waffle] Processing result for player score [{player.score}]")
        result = process_result(group, player)
        redis.set_complex(group.name, result.group)

        log.debug(f"[handle_waffle] Building response for group [{result.group.name}]")
        to_channel = event.channel
        response = present(result.text, to_channel)

        say(response)
        return Response(messages.load("event.request.handled"), status=200)

    def get_group(event):
        """ Fetch group object from redis """
        group_id = event.team
        group = redis.get_complex(group_id, Group)
        if group is not None:
            log.debug(f"[get_group] Group found with id [{group_id}]")
            return group
        else:
            log.debug(f"[get_group] Creating new group with id [{group_id}]")
            dummy_king = Player("", -1, 0)
            group = Group(group_id, [], dummy_king, [])
            redis.set_complex(group_id, group)
            return group

    def get_player(event, group):
        """ Fetch player object from redis that corresponds to message sender """
        slack_user_url = config.SLACK_API.format("users.info?user=" + event.user)
        try:
            result = requests.get(slack_user_url, headers={'Authorization': 'Bearer ' + config.BOT_TOKEN})
            user = result.json().get("user").get("real_name").split()[0]
            potential_player = [p for p in group.players if p.name == user]

            if not potential_player:
                player = Player(user, 0, 0)
                group.players.append(player)
                redis.set_complex(group.name, group)
                log.debug(f"[get_player] [{user}] added to the system")
                return player

            else:
                return potential_player[0]

        except SlackApiError as e:
            log.error(f"Error fetching user! [{str(e)}]")

    def process_result(group, player):
        group.update_player(player)
        group.update_scroll(player)

        # Player is the King...
        if player.name == group.king.name:
            # ...and loses
            if player.streak == 0:
                log.info(f"[process_result] The Reign of King {player.name} is over!")
                log.info("[process_result] Searching for a new King...")
                group.dethrone()
                text = messages.load_with_params("result.king.lose", [player.name])
            # ...and wins
            else:
                text = messages.load_with_params("result.king.win", [str(player.score)])

        # Player is a commoner...
        else:
            # ...and loses
            if player.streak == 0:
                log.info(f"[process_result] The Streak of {player.name} has been broken!")
                text = messages.load_with_params("result.common.lose", [player.name])
            # ...and wins...
            else:
                # ...and deserves coronation
                if player.streak > group.king.streak:
                    group.crown(player)
                    text = messages.load_with_params("result.common.coronation", [player.name])
                else:
                    text = messages.load_with_params("result.common.win", [player.name, str(player.score)])

        result = namedtuple("Result", "group text")
        return result(group, text)

    def present(result, to_channel):
        message = {
            "ts": '',
            "channel": to_channel,
            "icon_emoji": ":robot_face:",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                                result + " :blush:\n\n"
                                         "*I am under development*"
                        ),
                    },
                }
            ],
        }
        return message

    # Blueprint return
    return archbishop
