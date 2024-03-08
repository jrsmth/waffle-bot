import logging
from json import JSONDecodeError
import jsonpickle
from flask_redis import FlaskRedis
from upstash_redis import Redis as UpstashRedis
from src.app.model.base import Base


class RedisClient:
    """ Wrapper functionality for the Redis Client """

    def __init__(self, app, url, token):
        self.log = logging.getLogger(__name__)
        self.client = UpstashRedis(url=url, token=token) if "upstash" in url \
            else FlaskRedis(app, decode_responses=True)

    def get_client(self):
        """ Return the redis client object """
        return self.client

    def get(self, key):
        """ Get an element by its key """
        value = self.client.get(key)
        if value is None:
            return None
        else:
            return self.client.get(key)

    def set(self, key, value):
        """ Set a key-value element """
        return self.client.set(key, value)

    def set_complex(self, key, complex_value):
        """ Set a complex key-value element by converting to json string """
        json_value = jsonpickle.encode(complex_value, unpicklable=False)
        self.log.debug("[set_complex] Successful conversion to JSON, setting value: " + json_value)
        return self.client.set(key, json_value)

    def get_complex(self, key, cls: Base):
        """ Get a complex key-value element and return as dictionary """
        json_value = self.client.get(key)
        if json_value is not None:
            try:
                return cls.from_json(json_value)
            except JSONDecodeError:
                raise Exception("[get_complex] Error parsing retrieved object: " + str(json_value))
        else:
            return None
