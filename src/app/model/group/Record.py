from src.app.model.base import Base


class Record(Base):
    """ Tracked Record for the Historic Streaks """
    name = ''
    streak = 0
    date = '0/0/0000'
