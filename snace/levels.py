from dataclasses import dataclass


@dataclass(frozen=True)
class Level:
    number: int
    name: str
    speed: int
    food_count: int = 1
    description: str = ""


LEVELS = [
    Level(number=1, name="Level 1", speed=100, food_count=1, description="Einfacher Start"),
    Level(number=2, name="Level 2", speed=100, food_count=2, description="Etwas schneller"),
    Level(number=3, name="Level 3", speed=100, food_count=2, description="Mehr Essen"),
    Level(number=4, name="Level 4", speed=100, food_count=2, description="Schnelleres Spiel"),
    Level(number=5, name="Level 5", speed=100, food_count=3, description="Schwieriger"),
    Level(number=6, name="Level 6", speed=100, food_count=3, description="Jetzt wird es ernst"),
]


def get_level(number: int):
    for level in LEVELS:
        if level.number == number:
            return level
    return None


def get_next_level(number: int):
    for index, level in enumerate(LEVELS):
        if level.number == number:
            if index + 1 < len(LEVELS):
                return LEVELS[index + 1]
            return None
    return None
