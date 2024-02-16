import pytest


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
def app():
    # required here to avoid premature creation - is create_app being interpreted when imported?
    from src.app.app import create_app

    return create_app()


@pytest.mark.skip(reason="Bolt needs to be mocked out...")
def test_hello(fake_envs, app):
    # order of fixtures is important

    test_client = app.test_client()
    response = test_client.get('/')

    assert response.status_code == 200
