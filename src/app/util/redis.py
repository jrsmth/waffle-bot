import logging
from json import JSONDecodeError
import jsons
from flask_redis import FlaskRedis
from upstash_redis import Redis as UpstashRedis


class RedisClient:
    """ Wrapper functionality for the Redis Client """

    def __init__(self, app, url, token):
        self.log = logging.getLogger(__name__)
        self.client = UpstashRedis(url=url, token=token) if "upstash" in url else FlaskRedis(app)

    def get_client(self):
        """ Return the redis client object """
        return self.client

    def get(self, key):
        """ Get an element by its key and decode in utf-8 format """
        value = self.client.get(key)
        if value is None:
            return None
        else:
            return self.client.get(key)  # .decode('utf-8') Note :: .decode() supported by Flask but not Upstash(?)
            # Question :: Can utf-8 decode happen at client instantiation?

    def set(self, key, value):
        """ Set a key-value element """
        return self.client.set(key, value)

    def set_complex(self, key, complex_value):
        """ Set a complex key-value element by converting to json string """
        json_value = standardise(jsons.dump(complex_value))
        self.log.debug("[set_complex] Successful conversion to JSON, setting value: " + json_value)
        return self.client.set(key, json_value)

    def get_complex(self, key):
        """ Get a complex key-value element by converting from json string """
        json_value = self.client.get(key)
        if json_value is None:
            return None
        else:
            json_value = json_value  # .decode('utf-8') Note :: .decode() supported by Flask but not Upstash(?)
            # Question :: Can utf-8 decode happen at client instantiation?
        try:
            return jsons.loads(standardise(json_value))
        except JSONDecodeError:
            raise Exception("[get_complex] Error parsing retrieved object: " + str(json_value))

    def clear(self):
        """ Remove all entries held in Redis """
        for key in self.client.scan_iter():
            self.client.delete(key)


def standardise(value):  # FixMe :: bit dodgy
    """ Standardises a JSON string for conversion into a python dict """

    # Convert Python `True/False/None` to JSON-standard `true/false/null`
    standardised = str(value) \
                    .replace("False,", "false,") \
                    .replace("False}", "false}") \
                    .replace("True,", "true,") \
                    .replace("True}", "true}") \
                    .replace("None,", "null,") \
                    .replace("None}", "null}")

    # Convert single-speech (') marks to the JSON-standard double-speech marks (")
    return standardised.replace("{\'", "{\"") \
        .replace("\'}", "\"}") \
        .replace("\':", "\":") \
        .replace(" \'", " \"") \
        .replace("\',", "\",")
