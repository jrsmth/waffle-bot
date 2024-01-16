import logging
import os
from json import JSONDecodeError
import jsons
from flask import current_app
# from flask_redis import FlaskRedis
from upstash_redis import Redis


# Wrapper functionality for the Flask Redis Client
class RedisClient:

    def __init__(self, app):
        # self.client = FlaskRedis(app)
        self.log = logging.getLogger(__name__)
        self.client = Redis(
            url=current_app.config.get("REDIS_URL"),
            token=os.environ.get("REDIS_TOKEN")
        )

    def get_client(self):
        return self.client

    # Get an element by its key and decode in utf-8 format
    def get(self, key):
        # return self.client.get(key).decode('utf-8')
        return self.client.get(key)

    # Set a key-value element
    def set(self, key, value):
        return self.client.set(key, value)

    # Set a complex key-value element by converting to json string
    def set_complex(self, key, complex_value):
        json_value = standardise(jsons.dump(complex_value))
        self.log.debug("[set_complex] Successful conversion to JSON, setting value: " + json_value)
        return self.client.set(key, json_value)

    # Get a complex key-value element by converting from json string
    def get_complex(self, key):
        # json_value = self.client.get(key).decode('utf-8')
        json_value = self.client.get(key)
        if json_value is None:
            return None

        try:
            return jsons.loads(standardise(json_value))
        except JSONDecodeError:
            raise Exception("[get_complex] Error parsing retrieved object: " + str(json_value))

    # Remove all entries held in Redis
    def clear(self):
        for key in self.client.scan_iter():
            self.client.delete(key)


# Standardises a JSON string for conversion into a python dict
def standardise(value):  # FixMe :: bit dodgy
    # Convert Python `False` to JSON-standard `true`
    standardised = str(value).replace("False,", "false,").replace("True,", "true,")

    # Convert single-speech (') marks to the JSON-standard double-speech marks (")
    return standardised.replace("{\'", "{\"") \
        .replace("\'}", "\"}") \
        .replace("\':", "\":") \
        .replace(" \'", " \"") \
        .replace("\',", "\",")
