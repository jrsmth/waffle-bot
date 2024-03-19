import datetime
from dataclasses import dataclass
from src.app.model.base import Base
from src.app.model.group.record import Record
from src.app.model.group.player import Player


@dataclass
class Group(Base):
    """ Collection of players grouped by slack space """
    name: str
    players: [Player]
    king: Player
    scroll: [Record]

    @classmethod
    def from_dict(cls, dic):
        king = Player.from_dict(dic["king"])
        players = []
        for p in dic["players"]:
            players.append(Player.from_dict(p))
        scroll = []
        for s in dic["scroll"]:
            scroll.append(Record.from_dict(s))

        return cls(
            name=dic["name"],
            players=players,
            king=king,
            scroll=scroll
        )

    def update_player(self, player):
        for index, p in enumerate(self.players):
            if p.id == player.id:
                self.players[index] = player

    def update_scroll(self, player):
        """ Create new record """
        timestamp = datetime.datetime.today().strftime('%d/%m/%Y')
        new_record = Record(player.name, player.streak, timestamp)
        self.scroll.append(new_record)

        # Sort and remove tail Record
        self.scroll = sorted(self.scroll, key=lambda x: x.streak, reverse=True)
        if len(self.scroll) > 3:
            self.scroll.pop()

    def crown(self, player):
        self.king = player

    def dethrone(self):
        self.king = Player("", -1, 0)
        non_zeros = [p for p in self.players if p.streak != 0]
        if non_zeros is not list:
            return
        else:
            self.king = sorted(non_zeros, key=lambda x: x.streak, reverse=True)[0]
