import os
import logging

import requests
from flask import Flask, Response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from flask import request as flask_request
from src.config.config import Config, DevConfig, ProductionConfig
from src.model.group import Group
from src.model.player import Player
from src.util.redis import RedisClient


# Initialise app
app = Flask(__name__)


# Initialise config
bot_token = os.environ['BOT_TOKEN']
verify_token = os.environ['VERIFICATION_TOKEN']
secret = os.environ['SLACK_SIGNING_SECRET']
env = os.environ.get("FLASK_ENV")
redis_token = os.environ.get("REDIS_TOKEN")
slack_auth = 'Bearer ' + bot_token
slack_api = 'https://slack.com/api/{}'

if not env:
    raise ValueError("Start-up failed: no environment specified!")
elif env == "local":
    app.config.from_object(Config())
elif env == "dev":
    app.config.from_object(DevConfig())
elif env == "prod":
    app.config.from_object(ProductionConfig())
print(f"Starting app in [{env}] mode")
app.app_context().push()


# Initialise slack
slack_client = WebClient(token=bot_token)
slack_events_adapter = SlackEventAdapter(secret, "/event", app)


# Initialise redis
redis = RedisClient(app)


@app.route("/", methods=['GET'])
def hello():
    """ Test request (for spinning server up after inactivity) """
    return Response(str(redis.get_complex("T06DQBGR53J")), status=200)


@app.route('/event', methods=['POST'])
def handle_event():
    """ Handle event request from Slack """
    payload = flask_request.get_json()
    print(str(payload))

    if payload["token"] != verify_token:
        return Response("Invalid Token!", status=403)

    if "type" in payload:
        if payload["type"] == "url_verification":
            return Response(payload['challenge'], status=200)

    return Response(status=200)


@slack_events_adapter.on("message")
def handle_message(event):
    if is_waffle_event(event):
        group = get_group(event)
        player = get_player(event, group)
        streak = get_streak(event)
        king_streak = group["king"]["streak"]

        player.streak = streak
        text = 'Another battlefield conquered, well done {}!'.format(player.name)

        if streak == 0 and player_is_king(player, group):
            text = "Unlucky {}! The time has come to crown a new King".format(player.name)
            
            group["king"] = set_new_king(group)
        elif streak == 0:
            text = "Unlucky {}! Your kingdom must rebuild!".format(player.name)
            
        if int(king_streak) < int(streak):
            text = "Vive Rex! The WaffleCrown now rests on your head {}".format(player.name)
            king_streak = player.streak
            group["king"] = player

        redis.set_complex(group["name"], group)
        message = build_message(text)
        res = requests.post(slack_api.format("chat.postMessage"), headers={'Authorization': slack_auth}, json=message)
        print(res)

    return Response(status=200)

def player_is_king(player, group):
    king = group["king"]
    return player.name == king["name"]

def is_waffle_event(event):
    event_string = str(event)
    key_word = "#waffle"
    return key_word in event_string


def get_group(event):
    group_id = event.get("team_id")
    if redis.get_complex(group_id) is None:
        group = Group()
        group.name = group_id
        redis.set_complex(group_id, group)

    return redis.get_complex(group_id)


def get_player(event, group):
    user_id = event.get("event").get("user")
    try:
        result = requests.get(slack_api.format("users.info?user="+user_id), headers={'Authorization': slack_auth})
        user = result.json().get("user").get("real_name").split()[0]
        
        filtered_player = get_filtered_player(user, group)

        if not filtered_player:
            print("New player, {}, added to the system".format(user))
            return new_player(user, group)
        else:
            return Player(filtered_player)
    except SlackApiError as e:
        print("Error fetching user")

def get_filtered_player(user, group):
    for player in group["players"]:
        if player["name"] == user:
            return player

def new_player(user, group):
    player = Player()
    player.name = user
    group["players"].append(player)
    redis.set_complex(group["name"], group)
    return player

def get_streak(event):
    blocks = event.get("event").get("blocks")
    elements = blocks[0].get("elements")
    elements = elements[0].get("elements")
    streak = [elem for elem in elements if ('text' in elem and "streak" in elem.get("text"))][0]
    streak = str(streak.get("text").split(" ")[2]).strip('\n')
    print(streak)
    return int(streak)

def remove_current_king(group, player):
    for p in group["players"]:
        if p == player:
            player["streak"] = 0

def set_new_king(group):
    remove_current_king(group, group["king"])
    new_king = Player({"streak": -1})
    for p in group["players"]:
        if p["streak"] > new_king.streak:
            p = new_king
    return new_king

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


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
