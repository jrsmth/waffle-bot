import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
import jsons as jsons


@dataclass
class Base(ABC):
    """ Model Base Class """

    @classmethod
    @abstractmethod
    def from_dict(cls, dic):
        """ Convert a dictionary to a python object """
        pass

    @classmethod
    def from_json(cls, json_str: str):
        """ Convert a json string to a python object """
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def to_string(cls):
        """ Converts a complex object into a string """
        return str(jsons.dump(cls))
