import hashlib
import hmac

import fakeredis
import pytest
import time

from flask import Flask
from from_root import from_root
from unittest.mock import patch, Mock

from slack_bolt.app.app import App

from src.app.archbishop.archbishop import construct_blueprint
from src.app.archbishop import archbishop
from src.app.model.group.group import Group
from src.app.model.group.player import Player
from json import loads
from src.app.util.messages import Messages
from src.app.util.redis import RedisClient


@pytest.fixture
def fake_envs(monkeypatch):
    monkeypatch.setenv('REDIS_TOKEN', 'REDIS_TOKEN')
    monkeypatch.setenv('REDIS_URL', 'redis://REDIS_URL')
    monkeypatch.setenv('SLACK_BOT_TOKEN', 'BOT_TOKEN')
    monkeypatch.setenv('SLACK_SIGNING_SECRET', 'SLACK_SECRET')
    monkeypatch.setenv('SLACK_SCOPES', '["SCOPE_ONE", "SCOPE_2"]')
    monkeypatch.setenv('DEBUG', 'False')
    monkeypatch.setenv('PORT', '3000')


@pytest.fixture()
def local_only_envs(monkeypatch):
    monkeypatch.setenv('REDIS_TOKEN', '')
    monkeypatch.setenv('REDIS_URL', 'redis://@localhost:6379')
    monkeypatch.setenv('SLACK_BOT_TOKEN', 'put the real token in here yourself')
    monkeypatch.setenv('SLACK_SIGNING_SECRET', 'put the real signing secret in here yourself')
    monkeypatch.setenv('SLACK_SCOPES', '["channels:history", "chat:write", "groups:history", "im:write", "pins:read", "users:read"]')
    monkeypatch.setenv('DEBUG', 'False')
    monkeypatch.setenv('PORT', '3000')


@pytest.mark.skip(reason="Bolt needs to be mocked out...")
def test_hello(fake_envs):
    # order of fixtures is important

    test_client = app.test_client()
    response = test_client.get('/')

    assert response.status_code == 200


@patch("src.app.util.redis.FlaskRedis")
def test_process_result_group_king_loss(flask_redis_patch, local_only_envs):
    """A player, who is currently leading in a group of many, submits a loss"""

    app = Flask(__name__)

    import src.app.config.config as cfg
    config = cfg.Config()
    app.config.from_object(config)
    app.app_context().push()

    fake_redis = fakeredis.FakeRedis()

    # starting_group = Group(
    #     {
    #         "name": "groupid",
    #         "king": Player({"name": "Hayden", "score": 4, "streak": 10}),
    #         "players": [
    #             Player({"name": "playerid", "score": 4, "streak": 10})
    #         ],
    #         "scroll": [
    #             {"date": "0/0/0000", "name": "", "streak": 0},
    #             {"date": "0/0/0000", "name": "", "streak": 0},
    #             {"date": "0/0/0000", "name": "", "streak": 0}
    #         ]
    #     }
    # )

    flask_redis_patch.get = Mock(side_effect=fake_redis.get)
    flask_redis_patch.set = Mock(side_effect=fake_redis.set)

    redis = RedisClient(app, config.REDIS_URL, config.REDIS_TOKEN)
    redis.client = flask_redis_patch
    # redis.set_complex("groupid", starting_group)

    # Requests are made at points:
    # App._init_middleware_list (line 383) 'auth_test_result = self._client.auth_test(token=self._token)
    bolt = App(
        token=config.BOT_TOKEN,
        signing_secret=config.SIGNING_SECRET,
        # TODO: Implement signature/timestamp generation to pass internal validation
    )
    messages = Messages(from_root("resources", "messages.properties"))

    blueprint = archbishop.construct_blueprint(bolt, config, messages, redis)
    app.register_blueprint(blueprint)

    test_client = app.test_client()

    with open('src/app/archbishop/test_resources/submission.json', 'r') as submission_file:
        submission_str = submission_file.read().replace('\r', '')

    body = loads(submission_str)
    now = time.time()
    timestamp = int(now)
    format_req = str.encode(f"v0:{now}:{str(body)}")
    encoded_secret = str.encode(config.SIGNING_SECRET)
    request_hash = hmac.new(encoded_secret, format_req, hashlib.sha256).hexdigest()
    signature = f"v0={request_hash}"

    response = test_client.post(config.EVENT_PATH, headers={"X-Slack-Signature": signature, "X-Slack-Request-Timestamp": timestamp}, json=body)

    group_json = '{"king": {"name": "Hayden", "score": 4, "streak": 10}, "name": "T06DQBGR53J", "players": [{"name": "Hayden", "score": 4, "streak": 10}], "scroll": [{"date": "0/0/0000", "name": "", "streak": 0}, {"date": "0/0/0000", "name": "", "streak": 0}, {"date": "0/0/0000", "name": "", "streak": 0}]}'




def test_process_result_group_commoner_surpasses_king():
    """A player, whose streak is lesser than the group's king, submits a streak higher than that king"""
    pass


def test_process_result_group_commoner_retain_status():
    """A player, whose streak is lesser than the group's king, submits a streak that is lower than that king"""
    pass


def test_process_result_group_commoner_loses():
    """A player, whose streak is lesser than the group's king, submits a loss"""
    pass

