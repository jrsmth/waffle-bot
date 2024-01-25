from src.app.model.base import Base


class Record(Base):
    """ Tracked player information """
    name = ''
    streak = 0
    date = '0/0/0000'

    # def __init__(self, name, streak, date):
    #     self.name = name
    #     self.streak = streak
    #     self.date = date
