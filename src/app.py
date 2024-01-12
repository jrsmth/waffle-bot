import os
import logging

import requests
from flask import Flask, Response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from flask import request as flask_request


# Initialise config
bot_token = os.environ['BOT_TOKEN']
verify_token = os.environ['VERIFICATION_TOKEN']
secret = os.environ['SLACK_SIGNING_SECRET']


# Initialise flask
app = Flask(__name__)


# Initialise slack
slack_client = WebClient(token=bot_token)
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
    print(str(event))

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

    # slack_client.chat_postMessage(
    #     channel=channel_id,
    #     text="Hello from Render, you son of a b*tch"
    # )
    auth = 'Bearer ' + bot_token
    slack_api = 'https://slack.com/api/chat.postMessage'
    message = {"channel": "#bot-tester", "text": "Hello from Render, you son of a b*tch"}
    print("hit 2")
    res = requests.post(slack_api, headers={'Authorization': auth}, json=message)
    print(str(res.json()))

    return Response(status=200)


@slack_events_adapter.on("message")
def handle_message(event):
    user_id = event.get("event").get("user")
    event_string = str(event)
    print(event_string) # TODO :: implement logging
    auth = 'Bearer ' + bot_token
    slack_api = 'https://slack.com/api/{}'
    print(user_id)

    if "#waffle" in event_string:
        user = 'the King'
        try:
            # result = slack_client.users_info(user=user_id)
            # logger.info(result)
            result = requests.get(slack_api.format("user.info?user="+user_id), headers={'Authorization': auth})
            print(str(result.json()))
            user = result.json().get("user").get("real_name").split()[0]
        except SlackApiError as e:
            print("Error fetching user")
            # logger.error("Error fetching user: {}".format(e))

        text = "Long live {}!".format(user)
        if ":broken_heart: streak: 0" in str(event):
            text = "The time has come to crown a new King"

        message = {"channel": "#bot-tester", "text": text}
        res = requests.post(slack_api.format("chat.postMessage"), headers={'Authorization': auth}, json=message)

    return Response(status=200)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
