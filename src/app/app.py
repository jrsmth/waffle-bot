import json
from logging.config import dictConfig
from flask import Flask, current_app
from from_root import from_root
from slack_bolt import App
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

    # Initialise bolt
    bolt = App(
        token=config.BOT_TOKEN,
        signing_secret=config.SIGNING_SECRET
    )

    # Initialise redis
    redis = RedisClient(app, config.REDIS_URL, config.REDIS_TOKEN)

    # Initialise logger
    dictConfig(json.load(open(from_root("app", "config", "logs.json"))))
    app.logger_name = "waffle-bot"

    # Initialise messages
    messages = Messages(from_root("resources", "messages.properties"))

    # Initialise archbishop
    app.register_blueprint(archbishop.construct_blueprint(bolt, config, messages, redis))

    return app


# Create Flask app
app = create_app()

# Only use when running direct
if __name__ == "__main__":
    app.run(
        port=current_app.config["PORT"],
        debug=current_app.config["DEBUG"],
    )
