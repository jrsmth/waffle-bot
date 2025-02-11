import logging

import requests
from flask import Blueprint, Response
from flask import request
from slack_sdk.errors import SlackApiError
from src.app.model.event.event import Event
from src.app.model.group.group import Group
from src.app.model.group.player import Player
from src.app.deacon.deacon import handle_king, handle_commoner
from collections import namedtuple
from slack_bolt.adapter.flask import SlackRequestHandler

import shortuuid


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
        group_id = request.form["team_id"]
        group = redis.get_complex(group_id, Group)
        if group is None:
            return Response("Cannot find group with id " + group_id, status=400)
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
        group = redis.get_complex(group_id, Group)
        if group is None:
            return Response("Cannot find group with id " + group_id, status=400)
        return Response(str(group), status=200)

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
        event_score = event.get_score()
        event_streak = event.get_streak()

        if event.has_no_waffle_data():
            log.debug("[handle_waffle] Disregarding event, could not extract waffle data")
            return

        group = get_group(event)
        player = get_player(event, group)

        log.debug(f"[handle_waffle] Updating player information for [{player.name}]")
        player.score += event_score
        if event_streak == 0:
            player.prev_streak = player.streak
        player.streak = event_streak
        player.games += 1

        log.debug(f"[handle_waffle] Processing result for player score [{player.score}]")
        result = process_result(group, player)
        redis.set_complex(group.name, result.group)

        log.debug(f"[handle_waffle] Building response for group [{result.group.name}]")
        to_channel = event.channel
        response = present(result.text, to_channel)

        say(response)

    def get_group(event):
        """ Fetch group object from redis """
        group_id = event.team
        group = redis.get_complex(group_id, Group)
        if group is not None:
            log.debug(f"[get_group] Group found with id [{group_id}]")
            return group
        else:
            log.debug(f"[get_group] Creating new group with id [{group_id}]")
            dummy_king = "Dummy King"
            group = Group(group_id, [], dummy_king, [])
            redis.set_complex(group_id, group)
            return group

    def get_player(event, group):
        """ Fetch player object from redis that corresponds to message sender """
        slack_user_url = config.SLACK_API.format("users.info?user=" + event.user)
        try:
            result = requests.get(slack_user_url, headers={'Authorization': 'Bearer ' + config.BOT_TOKEN})
            user = result.json().get("user")
            user_name = user.get("real_name")
            user_id = user.get("id")
            potential_player = [p for p in group.players if p.id == user_id]

            if not potential_player:
                player = Player(user_id, user_name, 'Newbie', 0, shortuuid.uuid(), 0, 0, 0)
                group.players.append(player)
                redis.set_complex(group.name, group)
                log.debug(f"[get_player] [{user_name}] added to the system with id [{user_id}]")
                return player

            else:
                return potential_player[0]

        except SlackApiError as e:
            log.error(f"Error fetching user! [{str(e)}]")

    def process_result(group, player):
        group.update_player(player)
        group.update_scroll(player)

        # Player is the King...
        if player.id == group.king:
            log.debug(f"[process_result] Consulting Deacon to handle King with Id [{group.king}")
            text = handle_king(log, messages, group, player)
        # Player is a commoner...
        else:
            log.debug(f"[process_result] Consulting Deacon to handle Player with Id [{player.id}")
            text = handle_commoner(log, messages, group, player)

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
                        "text": f"{result}"
                    },
                }
            ],
        }
        return message

    # Blueprint return
    return archbishop
