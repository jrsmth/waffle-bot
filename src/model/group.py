from src.model.base import Base
from src.model.player import Player


# Collection of players grouped by space
class Group(Base):
    name = ''
    players = []
    king = Player()
