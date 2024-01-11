import os
import logging
from flask import Flask, Response
from flask import request as flask_request
from slack import WebClient
from slackeventsapi import SlackEventAdapter


# Initialise config
token = os.environ['BOT_TOKEN']
secret = os.environ['SLACK_SIGNING_SECRET']


# Initialise flask
app = Flask(__name__)


# Initialise slack
slack_client = WebClient(token)
slack_events_adapter = SlackEventAdapter(secret, "/slack/events", app)


@app.route("/", methods=['GET'])
def hello():
    """ Test request for spinning server up after inactivity """
    return Response("Hello, World!"), 200


@app.route('/challenge', methods=['POST'])
def challenge():
    """ Authentication challenge from Slack """
    payload = flask_request.get_json()

    print(str(payload))

    if payload:
        return Response(payload['challenge']), 200


@slack_events_adapter.on("pin_added")
def handle_pin_added(event, client):
    print("hit 1")

    channel_id = event.get("channel_id")
    user_id = event.get("user")
    message = {
        "ts": '',
        "channel": channel_id,
        "username": user_id,
        "icon_emoji": ":robot_face:",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "Welcome to Slack! :wave: We're so glad you're here. :blush:\n\n"
                        "*Get started by completing the steps below:*"
                    ),
                },
            }
        ],
    }

    client.chat_update(**message)
    print("hit 2")

    return Response(status=200)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
