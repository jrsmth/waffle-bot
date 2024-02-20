import re

from munch import Munch

from src.app.model.base import Base


class Element(Base):
    type = ""
    text = ""
    unicode = ""


class OuterElement(Base):
    type = ""
    elements = [Element()]


class Block(Base):
    elements = [OuterElement()]


class Event(Base):
    """ Enhanced message event object based on Slack's Event API """
    type = ""
    user = ""
    blocks = [Block()]
    team = ""
    channel = ""

    def get_score(self):
        block: Block = Munch.fromDict(self.blocks[0])
        elements: [Element] = block.elements[0].elements
        score_text = [elem for elem in elements if (hasattr(elem, "text") and "/5" in elem.text)][0].text
        score = re.split(' ', score_text, 1)[1][0]
        return int(0 if score == 'X' else score[0])

    def get_streak(self):
        block: Block = Munch.fromDict(self.blocks[0])
        elements: [Element] = block.elements[0].elements
        streak_element: Element = [elem for elem in elements if (hasattr(elem, "text") and "streak" in elem.text)][0]
        return int(streak_element.text.split(" ")[2].strip("\n"))
