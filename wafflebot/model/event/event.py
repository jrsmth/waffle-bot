import re
from wafflebot.model.base import Base


class Element(Base):
    type = ""
    text = ""
    unicode = ""


class OuterElement(Base):
    type = ""
    elements = [Element()]


class Block(Base):
    elements = [OuterElement()]


class Message(Base):
    text = ""
    ts = ""
    type = ""
    user = ""
    blocks = [Block()]


class Event(Base):
    """ Enhanced events object based on Slack's Event API """
    team_id = ""
    event = Message()

    def get_score(self):
        elements = self.event.blocks[0].elements[0].elements
        score_text = [elem for elem in elements if (hasattr(elem, "text") and "/5" in elem.text)][0].text
        score = re.split(' ', score_text, 1)[1][0]
        return int(0 if score == 'X' else score[0])

    def get_streak(self):
        elements: [Element] = self.event.blocks[0].elements[0].elements
        streak_element: Element = [elem for elem in elements if (hasattr(elem, "text") and "streak" in elem.text)][0]
        return int(streak_element.text.split(" ")[2].strip("\n"))
