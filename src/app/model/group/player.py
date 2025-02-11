from dataclasses import dataclass
from datetime import datetime
from src.app.model.base import Base
from src.app.model.group.record import Record


@dataclass
class Player(Base):
    """ Tracked player information """
    id: str
    name: str
    title: str
    streak: int
    streak_id: str
    prev_streak: int
    score: int
    games: int

    @classmethod
    def from_dict(cls, dic):
        return cls(
            id=dic["id"],
            name=dic["name"],
            title=dic["title"],
            streak=dic["streak"],
            streak_id=dic["streak_id"],
            prev_streak=dic["prev_streak"],
            score=dic["score"],
            games=dic["games"]
        )
    def get_average(self):
        # Return average score to 2 decimal places
        return round(self.score / self.games, 2)

    def get_record(self):
        """ Convert a player into a record """
        return Record(self.name, self.streak, self.streak_id, datetime.today().strftime('%d/%m/%Y'))

