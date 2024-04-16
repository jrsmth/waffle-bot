import json
import os


class Config(object):
    # General
    DEBUG = os.environ['DEBUG']
    PORT = os.environ['PORT']

    # Redis Config
    REDIS_TOKEN = os.environ['REDIS_TOKEN']
    REDIS_URL = os.environ['REDIS_URL']

    # Slack Config
    BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
    SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
    SCOPES = json.loads(os.environ['SLACK_SCOPES'])
    SLACK_API = 'https://slack.com/api/{}'
    EVENT_PATH = '/event/'

    # Scroll limits
    SCROLL_MIN_STREAK = os.environ['SCROLL_MIN_STREAK']
    SCROLL_MAX_LIST = os.environ['SCROLL_MAX_LIST']