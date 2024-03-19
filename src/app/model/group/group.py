from datetime import datetime, timedelta
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

    DATE_FORMAT = '%d/%m/%Y'

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
            if p.name == player.name:
                self.players[index] = player

    def update_scroll(self, player):
        """ Create new record """
        scroll_entry_replaced = False
        timestamp = datetime.today().strftime(self.DATE_FORMAT)
        new_record = Record(player.name, player.streak, timestamp)

        for index in range(len(self.scroll)):
            if self.scroll_same_streak(index, player):
                self.scroll[index] = Record(player.name, player.streak, timestamp)
                scroll_entry_replaced = True

        if not scroll_entry_replaced:
            self.add_new_scroll(new_record)

    def scroll_same_streak(self, index, player):
        """ Compares current date and previous date """
        timestamp = datetime.today().strftime(self.DATE_FORMAT)
        timestamp_yesterday = (datetime.today() - timedelta(days=1)).strftime(self.DATE_FORMAT)
        return (self.scroll[index] == player.name and self.scroll[index] == player.streak - 1 or
                (self.scroll[index].date == timestamp_yesterday or self.scroll[index].date == timestamp))

    def add_new_scroll(self, new_record):
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
