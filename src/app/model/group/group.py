from dataclasses import dataclass
import shortuuid
from src.app.model.base import Base
from src.app.model.group.record import Record
from src.app.model.group.player import Player
from src.app.config.config import Config


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
        """ Update player and handle streak reset if necessary """
        for index, p in enumerate(self.players):
            if p.name == player.name:
                if player.streak == 0:
                    player.streak_id = shortuuid.uuid()
                self.players[index] = player

    def update_scroll(self, player):
        """ Update scroll if new streak is worthy """
        if self.__is_empty_scroll():
            self.scroll.append(player.get_record())
            return

        if self.__is_unworthy(player.streak):
            return

        if self.__is_active(player.streak_id):
            unsorted_scroll = [player.get_record() if x.streak_id == player.streak_id else x for x in self.scroll]
            self.scroll = sorted(unsorted_scroll, key=lambda x: x.streak, reverse=True)

        else:
            self.scroll.append(player.get_record())
            self.scroll = sorted(self.scroll, key=lambda x: x.streak, reverse=True)
            if len(self.scroll) > int(Config.SCROLL_MAX_LIST):
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
        """ Determine if streak is unworthy of scroll update """
        sorted_scroll = sorted(self.scroll, key=lambda x: x.streak, reverse=False)
        if new_streak < int(Config.SCROLL_MIN_STREAK):
            return True
        else:
            return len(self.scroll) == int(Config.SCROLL_MAX_LIST) and new_streak < sorted_scroll[0].streak

    def __is_active(self, streak_id):
        """ Determine if player streak is active in scroll by comparison with recorded streak ids """
        matching_ids = [x for x in self.scroll if x.streak_id == streak_id]
        return len(matching_ids) != 0

    def __is_empty_scroll(self):
        """ Determine if scroll is empty """
        return len(self.scroll) == 0
