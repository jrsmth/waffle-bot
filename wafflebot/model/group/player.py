from wafflebot.model.base import Base


class Player(Base):
    """ Tracked player information """
    name = ''
    streak = 0
    score = 0
