import os


class Config(object):
    # Redis Config
    REDIS_TOKEN = os.environ['REDIS_TOKEN']
    REDIS_URL = os.environ['REDIS_URL']

    # Slack Tokens
    BOT_TOKEN = os.environ['BOT_TOKEN']
    SECRET = os.environ['SLACK_SIGNING_SECRET']
    VERIFICATION_TOKEN = os.environ['VERIFICATION_TOKEN']

    # Slack API Config
    SLACK_API = 'https://slack.com/api/{}'
    SLACK_TOKEN = 'Bearer ' + BOT_TOKEN
    EVENT_PATH = '/event'
