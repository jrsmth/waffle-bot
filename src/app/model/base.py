import jsons as jsons
from munch import Munch


class Base:
    """ Model Base Class """

    def __init__(self, d=None):
        """ Constructor that optionally converts dict to obj """
        if d is not None:
            for key, value in d.items():
                if type(value) is dict:
                    setattr(self, key, Munch().fromDict(value))
                else:
                    setattr(self, key, value)

    def to_string(self):
        """ Converts a complex object into a string """
        return str(jsons.dump(self))
