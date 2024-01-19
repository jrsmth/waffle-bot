import jsons as jsons
from munch import Munch


# Model Base Class
class Base:

    # Constructor that optionally converts dict to obj
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                if type(value) is dict:
                    setattr(self, key, Munch().fromDict(value))
                else:
                    setattr(self, key, value)

    # Converts a complex object into string
    def to_string(self):
        return str(jsons.dump(self))
