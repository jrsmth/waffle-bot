import factories
import pytest
from fakeredis import FakeRedis
from unittest.mock import patch
from unittest.mock import MagicMock
from flask_redis import FlaskRedis
from pytest_redis import factories

redis_my_proc = factories.redis_proc(port=None)
redis_my = factories.redisdb('redis_my_proc')


@pytest.fixture()
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture()
def redis_mock():
    return patch("upstash_redis.Redis")


@pytest.fixture
def fake_envs(monkeypatch):
    monkeypatch.setenv('REDIS_TOKEN', "FAKEREDISTOKEN")
    monkeypatch.setenv('REDIS_URL', "redis://SOMEREDISURL")
    monkeypatch.setenv('BOT_TOKEN', "SOMEBOTTOKEN")
    monkeypatch.setenv('SLACK_SIGNING_SECRET', "SOMESIGNINGSECRET")
    monkeypatch.setenv('VERIFICATION_TOKEN', "SOMEVERIFICATIONTOKEN")


@pytest.fixture()
def test_envs(monkeypatch):
    monkeypatch.setenv('REDIS_TOKEN', "")
    monkeypatch.setenv('REDIS_URL', "redis://localhost")
    monkeypatch.setenv('BOT_TOKEN', "SOMEBOTTOKEN")
    monkeypatch.setenv('SLACK_SIGNING_SECRET', "SOMESIGNINGSECRET")
    monkeypatch.setenv('VERIFICATION_TOKEN', "SOMEVERIFICATIONTOKEN")


@pytest.fixture()
def app():
    # required here to avoid premature creation - is create_app being interpreted when imported?
    from src.app.app import create_app

    return create_app()


def test_hello(fake_envs, app):
    # order of fixtures is important

    test_client = app.test_client()
    response = test_client.get("/")

    assert response.status_code == 200


def test_get_group(redisdb, mocker, test_envs, redis_mock, app):
    # included with pytest-redis
    redisdb.set('test1', 'test')
    # included with pytest-mock - aiming to mock the FlaskRedis instance used in app's Redis client
    redis_mock = mocker.patch('src.app.util.redis.FlaskRedis', redisdb)

    test_client = app.test_client()

    response = test_client.get("/group/somegroup")

    assert redis_mock.get.assert_called_once_with("somegroup")
    assert response.status_code == 200
