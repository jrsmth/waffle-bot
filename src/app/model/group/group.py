from src.app.model.base import Base
from src.app.model.group.player import Player


class Group(Base):
    """ Collection of players grouped by slack space """
    name = ''
    players = []
    king = Player()

    def update_player(self, player):
        for index, p in enumerate(self.players):
            if hasattr(p, "name") and p.name == player.name:
                self.players[index] = player

    def crown(self, player):
        self.king = player

    def dethrone(self):
        self.king = Player({"streak": -1})

        non_zeros = [p for p in self.players if p["streak"] != 0]

        if non_zeros is not list:
            return
        else:
            self.king = non_zeros.sort(key=lambda x: x.streak, reverse=True)[0]
