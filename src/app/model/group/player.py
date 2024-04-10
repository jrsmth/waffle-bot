from dataclasses import dataclass

from src.app.model.base import Base


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
