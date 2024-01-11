from flask import Flask, Response
from flask import request as flask_request


app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    """ Test request for spinning server up after inactivity """
    return Response("Hello, World!"), 200


@app.route('/verify', methods=['POST'])
def challenge():
    """ Authentication challenge from Slack """
    payload = flask_request.get_json()

    if payload:
        return Response(payload['challenge']), 200
