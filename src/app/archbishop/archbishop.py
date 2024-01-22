import logging
import requests
from flask import Blueprint, Response
from flask import request as flask_request
from slack_sdk.errors import SlackApiError
from src.app.model.event.event import Event
from src.app.model.group.group import Group
from src.app.model.group.player import Player


# Archbishop Logic
def construct_blueprint(adapter, config, messages, redis):
    log = logging.getLogger(__name__)
    archbishop = Blueprint('archbishop', __name__)

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
        payload = flask_request.get_json()
        log.debug(f"[handle_event] New Event from Slack! [{str(payload)}]")

        if payload["token"] != config.VERIFICATION_TOKEN:
            return Response("Invalid Token!", status=403)

        if "type" in payload:
            if payload["type"] == "url_verification":
                return Response(payload['challenge'], status=200)

        return Response(status=200)

    @adapter.on("message")
    def handle(new_message):
        """ Process new message according to its content """
        if should_ignore(new_message):
            return Response(messages.load("event.request.ignored"), status=200)

        else:
            event = Event(new_message)
            group = get_group(event)
            king_streak = group.king.streak
            player = get_player(event, group)
            player.score += 0  # event.get_score()
            player.streak = event.get_streak()

            result: tuple[Group, str] = process_result(group, player, king_streak)
            redis.set_complex(group.name, result[0])

            requests.post(
                config.SLACK_API.format("chat.postMessage"),
                headers={'Authorization': config.SLACK_TOKEN},
                json=build_message(result[1])
            )

            return Response(messages.load("event.request.handled"), status=201)

    def should_ignore(new_message):
        return messages.load("event.message.keyword") not in str(new_message)

    def get_group(event):
        """ Fetch group object from redis """
        group_id = event.team_id
        group = redis.get_complex(group_id)

        if group is None:
            group = Group()
            group.name = group_id
            redis.set_complex(group_id, group)

        return Group(group)

    def get_player(event, group):
        """ Fetch player object from redis that corresponds to message sender """
        slack_user_url = config.SLACK_API.format("users.info?user=" + event.event.user)
        try:
            result = requests.get(slack_user_url, headers={'Authorization': config.SLACK_TOKEN})
            user = result.json().get("user").get("real_name").split()[0]
            potential_player = [p for p in group.players if p.name == user]

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

        # Player is the King...
        if player.name == group.king.name:
            # ...and loses
            if player.streak == 0:
                log.info(f"[process_result] The Reign of King {player.name} is over!")
                log.info("[process_result] Searching for a new King...")
                group.dethrone(player)
                text = messages.load_with_params("result.king.lose", [player.name])
            # ...and wins
            else:
                text = messages["result.king.win"]

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
                    text = messages.load_with_params("result.common.win", [player.name, player.score])

        return group, text

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
