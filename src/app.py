import os
import logging
from flask import Flask, Response
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from flask import request as flask_request


# Initialise config
bot_token = os.environ['BOT_TOKEN']
verify_token = os.environ['VERIFICATION_TOKEN']
secret = os.environ['SLACK_SIGNING_SECRET']


# Initialise flask
app = Flask(__name__)


# Initialise slack
slack_client = WebClient(bot_token)
slack_events_adapter = SlackEventAdapter(secret, "/event", app)


@app.route("/", methods=['GET'])
def hello():
    """ Test request (for spinning server up after inactivity) """
    return Response("Hello, World!", status=200)


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

        # return Response("Internal Error!", status=500)
    return Response(status=200)


@slack_events_adapter.on("pin_added")
def handle_pin_added(event):
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

    slack_client.chat_update(**message)
    print("hit 2")

    return Response(status=200)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
