import logging
import re
from munch import Munch


class Element:
    type = ""
    text = ""
    unicode = ""


class OuterElement:
    type = ""
    elements = [Element()]


class Block:
    elements = [OuterElement()]


class Event:
    """ Enhanced message event object based on Slack's Event API """
    type = ""
    user = ""
    blocks = [Block()]
    team = ""
    channel = ""

    def __init__(self, d=None):
        """ Constructor that optionally converts dict to obj """
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

    def get_score(self):
        block: Block = Munch.fromDict(self.blocks[0])
        elements: [Element] = block.elements[0].elements
        score_text = self._search_elements_for_expr(elements, "#waffle[0-9]+ [X0-5]/[0-5]")
        if score_text is not None:
            score = re.split(' ', score_text, 1)[1][0]
            return int(0 if score == 'X' else score[0])

    def get_streak(self):
        block: Block = Munch.fromDict(self.blocks[0])
        elements: [Element] = block.elements[0].elements
        streak_text = self._search_elements_for_expr(elements, "streak: [0-9]*\n")
        if streak_text is not None:
            return int(streak_text.split(" ")[1].strip("\n"))

    def has_no_waffle_data(self):
        return self.get_score() is None or self.get_streak() is None

    @staticmethod
    def _search_elements_for_expr(elements, expr):
        for elem in elements:
            if hasattr(elem, "text") and re.search(expr, elem.text) is not None:
                return re.findall(expr, elem.text)[0]

