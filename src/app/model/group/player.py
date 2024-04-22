from dataclasses import dataclass

from src.app.model.base import Base


@dataclass
class Player(Base):
    """ Tracked player information """
    id: str
    name: str
    streak: int
    score: int
    games: int

    @classmethod
    def from_dict(cls, dic):
        return cls(
            id=dic["id"],
            name=dic["name"],
            streak=dic["streak"],
            score=dic["score"],
            games=dic["games"]
        )
    def get_average(self):
        # Return average score to 2 decimal places
        return round(self.score / self.games, 2)
