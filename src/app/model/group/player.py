from dataclasses import dataclass

from src.app.model.base import Base


@dataclass
class Player(Base):
    """ Tracked player information """
    name: str
    streak: int
    score: float
    played: int

    @classmethod
    def from_dict(cls, dic):
        return cls(
            name=dic["name"],
            streak=dic["streak"],
            score=dic["score"],
            played=dic["played"]
        )
