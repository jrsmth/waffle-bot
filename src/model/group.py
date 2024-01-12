from src.model.base import Base


# Collection of players grouped by space
class Group(Base):
    name = ''
    players = []
    king = ''
