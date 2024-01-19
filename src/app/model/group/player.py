from src.app.model.base import Base


# Tracked player information
class Player(Base):
    name = ''
    streak = 0
    score = 0
