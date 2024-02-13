from flask import Flask
import pytest

from src.app.config.config import Config


@pytest.fixture()
def app():
    app = Flask(__name__)

    config = Config()
