import json
from logging.config import dictConfig
from flask import Flask, current_app
from from_root import from_root
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
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
        signing_secret=config.SIGNING_SECRET,
        oauth_settings=OAuthSettings(
            client_id=config.CLIENT_ID,
            client_secret=config.CLIENT_SECRET,
            scopes=config.SCOPES,
            installation_store=FileInstallationStore(base_dir=config.INSTALLATION_DIR),
            state_store=FileOAuthStateStore(expiration_seconds=600, base_dir=config.STATE_DIR)
        )
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
