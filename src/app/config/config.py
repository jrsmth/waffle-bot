import json
import os


class Config(object):
    # Slack Client Config
    CLIENT_ID = os.environ['SLACK_CLIENT_ID']
    CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']
    SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
    SCOPES = json.loads(os.environ['SCOPES'])
    INSTALLATION_DIR = './data/installations'
    STATE_DIR = './data/states'

    # Redis Config
    REDIS_TOKEN = os.environ['REDIS_TOKEN']
    REDIS_URL = os.environ['REDIS_URL']

    # Slack API Config
    SLACK_API = 'https://slack.com/api/{}'
    EVENT_PATH = '/event/'

    # General
    DEBUG = os.environ['DEBUG']
    PORT = 3000
