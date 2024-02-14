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
    log = logging.getLogger(__name__)
    archbishop = Blueprint('archbishop', __name__)
    handler = SlackRequestHandler(bolt)

    @archbishop.route("/")
    def hello():
        """ Test request (useful for spinning server up after inactivity) """
        return Response("Hello, World!", status=200)

    @archbishop.route("/group/<group_id>")
    def group(group_id):
        """ Get group information by id """
        log.debug(f"[get_group] Retrieving group for id [{group_id}]")
        return Response(redis.get_complex(group_id), status=200)

    @archbishop.route(config.EVENT_PATH, methods=['POST'])
    def event():
        """ Handle event request from Slack """
        log.debug(f"[handle_event] New Event from Slack! [{str(request.get_json())}]")
        return handler.handle(request)

    @bolt.message(messages.load("event.message.keyword"))
    def handle(message, say): # Now naming not so good...
        # FixMe :: NO TRIGGER
        """ Process new message according to its content """
        # event = Event(new_message)
        # group = get_group(event)
        # king_streak = group.king.streak
        # player = get_player(event, group)
        # player.score += event.get_score()
        # player.streak = event.get_streak()
        #
        # result = process_result(group, player, king_streak)
        # redis.set_complex(group.name, result.group)

        # requests.post(
        #     config.SLACK_API.format("chat.postMessage"),
        #     headers={'Authorization': 'Bearer ' + config.BOT_TOKEN},
        #     json=build_message(result.text)
        # )

        user = message['user']
        say(f"Hi there, <@{user}>!")

        # return Response(messages.load("event.request.handled"), status=200)

    def get_group(event):
        """ Fetch group object from redis """
        group_id = event.team_id
        group = redis.get_complex(group_id)
        if group is not None:
            log.debug(f"[get_group] Group found with id [{group_id}]")
            return Group(group)
        else:
            log.debug(f"[get_group] Creating new group with id [{group_id}]")
            group = Group({"name": group_id})
            redis.set_complex(group_id, group)
            return group

    def get_player(event, group):
        """ Fetch player object from redis that corresponds to message sender """
        slack_user_url = config.SLACK_API.format("users.info?user=" + event.event.user)
        try:
            result = requests.get(slack_user_url, headers={'Authorization': 'Bearer ' + config.BOT_TOKEN})
            user = result.json().get("user").get("real_name").split()[0]
            potential_player = [p for p in group.players if p["name"] == user]

            if not potential_player:
                player = Player()
                player.name = user
                group.players.append(player)
                redis.set_complex(group.name, group)
                log.debug(f"[get_player] [{user}] added to the system")
                return player

            else:
                return Player(potential_player[0])

        except SlackApiError as e:
            log.error(f"Error fetching user! [{str(e)}]")

    def process_result(group, player, king_streak):
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
                if player.streak > king_streak:
                    group.crown(player)
                    text = messages.load_with_params("result.common.coronation", [player.name])
                else:
                    text = messages.load_with_params("result.common.win", [player.name, str(player.score)])

        Result = namedtuple("Result", "group text")
        return Result(group, text)

    def build_message(text):
        channel_id = '#bot-tester'
        message = {
            "ts": '',
            "channel": channel_id,
            "icon_emoji": ":robot_face:",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                                text + " :blush:\n\n"
                                       "*I am under development*"
                        ),
                    },
                }
            ],
        }
        return message

    # Blueprint return
    return archbishop
