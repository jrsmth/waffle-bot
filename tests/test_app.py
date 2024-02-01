

def test_hello(monkeypatch):
    monkeypatch.setenv('REDIS_TOKEN', "FAKEREDISTOKEN")
    monkeypatch.setenv('REDIS_URL', "redis://SOMEREDISURL")
    monkeypatch.setenv('BOT_TOKEN', "SOMEBOTTOKEN")
    monkeypatch.setenv('SLACK_SIGNING_SECRET', "SOMESIGNINGSECRET")
    monkeypatch.setenv('VERIFICATION_TOKEN', "SOMEVERIFICATIONTOKEN")

    from src.app.app import app

    test_client = app.test_client()
    response = test_client.get("/")
    print(response)

    assert response.status_code == 200
