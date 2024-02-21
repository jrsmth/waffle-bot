import datetime

from src.app.model.base import Base
from src.app.model.group.record import Record
from src.app.model.group.player import Player


class Group(Base):
    """ Collection of players grouped by slack space """
    name = ''
    players = []
    king = Player()
    scroll = [Record(), Record(), Record()]

    def update_player(self, player):
        for index, p in enumerate(self.players):
            if hasattr(p, "name") and p.name == player.name:
                self.players[index] = player

    def update_scroll(self, player, log):
        log.debug("[update_scroll] Score received, updating scroll!")
        # Create new record
        new_record = Record(
            {
                "name": player.name,
                "streak": player.streak,
                "date": datetime.datetime.today().strftime('%d/%m/%Y')
            }
        )
        scroll = self.scroll
        scroll.append(new_record)
        # Sort and remove tail Record
        log.debug(f"[update_scroll] Added to scroll! Scroll value: {scroll}")
        sorted_scroll = sorted(scroll, key=lambda x: x["streak"], reverse=True)
        log.debug(f"[update_scroll] Scroll sorted by streak! Scroll value: {scroll}")
        if(len(self.scroll) >= 3):
            self.scroll = sorted_scroll.pop()
            log.debug(f"[update_scroll] Too many Scroll entries, remove lowest score! Scroll value: {scroll}")

    def crown(self, player):
        self.king = player

    def dethrone(self):
        self.king = Player({"streak": -1})

        non_zeros = [p for p in self.players if p["streak"] != 0]

        if non_zeros is not list:
            return
        else:
            self.king = non_zeros.sort(key=lambda x: x.streak, reverse=True)[0]
