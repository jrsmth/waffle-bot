import json
from logging.config import dictConfig
from flask import Flask
from from_root import from_root
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
from wafflebot.config.config import Config
from wafflebot.util.messages import Messages
from wafflebot.util.redis import RedisClient
from wafflebot.archbishop import archbishop


def create_app():
    # Initialise app
    app = Flask(__name__)

    # Initialise config
    config = Config()
    app.config.from_object(config)
    app.app_context().push()

    # Initialise slack
    slack_client = WebClient(token=config.BOT_TOKEN)
    slack_events_adapter = SlackEventAdapter(config.SECRET, config.EVENT_PATH, app)

    # Initialise redis
    redis = RedisClient(app, config.REDIS_URL, config.REDIS_TOKEN)

    # Initialise logger
    dictConfig(json.load(open(from_root('wafflebot', 'config', 'logs.json'))))
    app.logger_name = 'waffle-bot'

    # Initialise messages
    messages = Messages(from_root('wafflebot', 'resources', 'messages.properties'))

    # Register blueprint
    app.register_blueprint(archbishop.construct_blueprint(slack_events_adapter, config, messages, redis))

    return app


# Let's go!
if __name__ == "__main__":
    app = create_app()
    app.run(port=3000)
else:
    gunicorn_app = create_app()
