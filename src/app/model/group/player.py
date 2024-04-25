from dataclasses import dataclass
from datetime import datetime
from src.app.model.base import Base
from src.app.model.group.record import Record


@dataclass
class Player(Base):
    """ Tracked player information """
    name: str
    streak: int
    streak_id: str
    score: int

    @classmethod
    def from_dict(cls, dic):
        return cls(
            name=dic["name"],
            streak=dic["streak"],
            streak_id=dic["streak_id"],
            score=dic["score"]
        )

    def get_record(self):
        """ Convert a player into a record """
        return Record(self.name, self.streak, self.streak_id, datetime.today().strftime('%d/%m/%Y'))
