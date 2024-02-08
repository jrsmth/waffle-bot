import json
from logging.config import dictConfig
from flask import Flask
from from_root import from_root
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
from src.app.config.config import Config
from src.app.util.messages import Messages
from src.app.util.redis import RedisClient
from src.app.archbishop import archbishop


def create_app():
    # Initialise app
    app = Flask(__name__)

    # Initialise config
    config = Config()
    app.config.from_object(config)
    app.app_context().push()

    # Initialise slack
    WebClient(token=config.BOT_TOKEN)
    slack_events_adapter = SlackEventAdapter(config.SECRET, config.EVENT_PATH, app)

    # Initialise redis
    redis = RedisClient(app, config.REDIS_URL, config.REDIS_TOKEN)

    # Initialise logger
    dictConfig(json.load(open(from_root('src', 'app', 'config', 'logs.json'))))
    app.logger_name = 'waffle-bot'

    # Initialise messages
    messages = Messages(from_root('src', 'app', 'resources', 'messages.properties'))

    # Register blueprint
    app.register_blueprint(archbishop.construct_blueprint(adapters, config, messages, redis))

    return app


# Create the Flask app
app = create_app()

# Only get to here when running directly
if __name__ == "__main__":
    app.run(port=3000)
