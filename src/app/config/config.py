import os


class Space(object):

    def __init__(self, space_name):
        self.space_name = space_name
        self.BOT_TOKEN = self.env('BOT_TOKEN')
        self.SECRET = self.env('SLACK_SIGNING_SECRET')
        self.VERIFICATION_TOKEN = self.env('VERIFICATION_TOKEN')

    def env(self, env_name):
        return os.environ[self.space_name+'_'+env_name]


class Config(object):
    # Redis Config
    REDIS_TOKEN = os.environ['REDIS_TOKEN']
    REDIS_URL = os.environ['REDIS_URL']

    # Slack Tokens
    spaces = [
        Space('TEST_WORKSPACE'),
        Space('TIER2_CONSULTING')
    ]

    # Slack API Config
    SLACK_API = 'https://slack.com/api/{}'
    EVENT_PATH = '/event'
