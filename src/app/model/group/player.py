from dataclasses import dataclass

from src.app.model.base import Base


@dataclass
class Player(Base):
    """ Tracked player information """
    id: str
    name: str
    streak: int
    score: int

    @classmethod
    def from_dict(cls, dic):
        return cls(
            id=dic["id"],
            name=dic["name"],
            streak=dic["streak"],
            score=dic["score"]
        )
