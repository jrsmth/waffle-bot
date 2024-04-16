import json
import os


class Config(object):
    # General
    DEBUG = os.getenv('DEBUG', 'False')
    PORT = os.getenv('PORT', '3000')

    # Redis Config
    REDIS_TOKEN = os.getenv('REDIS_TOKEN', 'REDIS_TOKEN')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://REDIS_URL')

    # Slack Config
    BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', 'BOT_TOKEN')
    SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET', 'SLACK_SECRET')
    SCOPES = json.loads(os.getenv('SLACK_SCOPES', '["SCOPE_ONE", "SCOPE_2"]'))
    SLACK_API = 'https://slack.com/api/{}'
    EVENT_PATH = '/event/'

    # Scroll limits
    SCROLL_MIN_STREAK = os.getenv('SCROLL_MIN_STREAK', '2')
    SCROLL_MAX_LIST = os.getenv('SCROLL_MAX_LIST', '3')