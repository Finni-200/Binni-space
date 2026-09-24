from dataclasses import dataclass


@dataclass(frozen=True)
class Level:
    number: int
    name: str
    speed: int
    food_count: int = 1
    description: str = ""
    minimum_length: int = 1


WINNER = 10


LEVELS = [
    Level(number=1, name="Level 1", speed=100, food_count=1, description="Einfacher Start", minimum_length=1),
    Level(number=2, name="Level 2", speed=100, food_count=2, description="Etwas schneller", minimum_length=5),
    Level(number=3, name="Level 3", speed=100, food_count=2, description="Mehr Essen", minimum_length=7),
    Level(number=4, name="Level 4", speed=100, food_count=2, description="Schnelleres Spiel", minimum_length=9),
    Level(number=5, name="Level 5", speed=100, food_count=2, description="Schwieriger", minimum_length=11),
    Level(number=6, name="Level 6", speed=100, food_count=2, description="Jetzt wird es ernst", minimum_length=13),
    Level(number=7, name="Level 7", speed=100, food_count=2, description="Die Schlange wird lang", minimum_length=15),
    Level(number=8, name="Level 8", speed=100, food_count=2, description="Nur noch wenige Schritte", minimum_length=17),
    Level(number=9, name="Level 9", speed=100, food_count=2, description="Fast geschafft", minimum_length=19),
    Level(number=WINNER, name="Gewonnen", speed=100, food_count=0, description="Du hast alle Level geschafft", minimum_length=20),
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


def get_level_for_length(length: int):
    for level in reversed(LEVELS):
        if length >= level.minimum_length:
            return level
    return LEVELS[0]
