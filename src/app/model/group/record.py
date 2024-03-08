from dataclasses import dataclass
from src.app.model.base import Base


@dataclass
class Record(Base):
    """ Tracked Record for the Historic Streaks """
    name: str
    streak: int
    date: str  # TODO :: actual date

    @classmethod
    def from_dict(cls, dic):
        return cls(
            name=dic["name"],
            streak=dic["streak"],
            date=dic["date"]
        )
