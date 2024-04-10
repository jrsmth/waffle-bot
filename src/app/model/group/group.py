from dataclasses import dataclass
from datetime import datetime

import shortuuid

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
            if p.name == player.name:
                if player.streak == 0:
                    player.streak_id = shortuuid.uuid()
                self.players[index] = player

    def update_scroll(self, player):
        """ Update scroll if new streak is worthy """
        if self.__is_unworthy(player.streak):
            return

        if self.__is_active(player.streak_id):
            existing_record = [x for x in self.scroll if x.streak_id == player.streak_id][0]
            existing_record.streak = player.streak
            existing_record.date = datetime.today().strftime('%d/%m/%Y')
            unsorted_scroll = [existing_record if x.streak_id == player.streak_id else x for x in self.scroll]
            self.scroll = sorted(unsorted_scroll, key=lambda x: x.streak, reverse=True)

        else:
            new_record = Record(player.name, player.streak, player.streak_id, datetime.today().strftime('%d/%m/%Y'))
            self.scroll.append(new_record)
            self.scroll = sorted(self.scroll, key=lambda x: x.streak, reverse=True)
            if len(self.scroll) > 3:
                self.scroll.pop()

    def crown(self, player):
        self.king = player

    def dethrone(self):
        self.king = Player("", -1, "", 0)
        non_zeros = [p for p in self.players if p.streak != 0]
        if len(non_zeros) == 0:
            return
        else:
            self.king = sorted(non_zeros, key=lambda x: x.streak, reverse=True)[0]

    def __is_unworthy(self, new_streak):
        """ Determine if streak is unworthy of scroll update by comparison to the lowest record """
        sorted_scroll = sorted(self.scroll, key=lambda x: x.streak, reverse=False)
        return len(sorted_scroll) == 0 or new_streak < sorted_scroll[0].streak

    def __is_active(self, streak_id):
        """ Determine if player streak is active in scroll by comparison with recorded streak ids """
        if len(self.scroll) != 0:
            matching_ids = [x for x in self.scroll if x.streak_id == streak_id]
            return len(matching_ids) != 0
        else: return False
