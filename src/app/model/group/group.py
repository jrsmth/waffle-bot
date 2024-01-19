from src.app.model.base import Base
from src.app.model.group.player import Player


# Collection of players grouped by slack space
class Group(Base):
    name = ''
    players = []
    king = Player()

    def update_player(self, player):
        players_without_this_one = [x for x in self.players if x.name != player.name]
        players_with_this_one = players_without_this_one.append(player)
        self.players = players_with_this_one

    def crown(self, player):
        self.king = player

    def dethrone(self):
        self.king = Player({"streak": -1})

        non_zeros = [p for p in self.players if p.streak != 0]

        if non_zeros is not list:
            return
        else:
            self.king = non_zeros.sort(key=lambda x: x.streak, reverse=True)[0]
