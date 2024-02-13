import requests

from example_code import get_yo_mamma_joke


def test_get_yo_mamma_joke(mocker):
    mock_response = {
        "joke": "Yo mamma so ugly she made One Direction go another direction."
    }

    mocker.patch("example_code.requests.get").return_value = mock_response

    response = get_yo_mamma_joke()

    requests.get.assert_called_once_with("https://www.yomama-jokes.com/api/v1/jokes/random")

    assert response == mock_response
