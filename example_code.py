import requests


def get_yo_mamma_joke():
    response = requests.get("https://www.yomama-jokes.com/api/v1/jokes/random")
    return response
