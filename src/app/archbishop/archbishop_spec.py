import pytest


@pytest.fixture
def fake_envs(monkeypatch):
    monkeypatch.setenv('REDIS_TOKEN', "FAKEREDISTOKEN")
    monkeypatch.setenv('REDIS_URL', "redis://SOMEREDISURL")
    monkeypatch.setenv('BOT_TOKEN', "SOMEBOTTOKEN")
    monkeypatch.setenv('SLACK_SIGNING_SECRET', "SOMESIGNINGSECRET")
    monkeypatch.setenv('VERIFICATION_TOKEN', "SOMEVERIFICATIONTOKEN")
    monkeypatch.setenv('DEBUG', "False")
    monkeypatch.setenv('PORT', "3000")


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
