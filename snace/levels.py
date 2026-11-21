from dataclasses import dataclass


@dataclass(frozen=True)
class Level:
    number: int
    name: str
    speed: int
    normal_f_c: int
    small_f_c: int 
    Angry_Bird_c: int 
    W: int 
    description: str 
    minimum_length: int 


WINNER = 10


LEVELS = [
    Level(number=1, name="Level 1", speed=100, normal_f_c=1, small_f_c=0, Angry_Bird_c=1, W=0, description="Einfacher Start", minimum_length=1),
    Level(number=2, name="Level 2", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=0, description="Zwei Essen", minimum_length=5),
    Level(number=3, name="Level 3", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=0, description="Mehr Essen in 10 sek", minimum_length=7),
    Level(number=4, name="Level 4", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=0, description="Mit Angry Birds", minimum_length=9),
    Level(number=5, name="Level 5", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=0, description="Angry Birds in 10 sek", minimum_length=11),
    Level(number=6, name="Level 6", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=0, description="Jetzt wird es schnell", minimum_length=13),
    Level(number=7, name="Level 7", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=1, description="Jezt kommen die Wände", minimum_length=15),
    Level(number=8, name="Level 8", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=1, description="Wände und small Essen", minimum_length=17),
    Level(number=9, name="Level 9", speed=100, normal_f_c=1, small_f_c=1, Angry_Bird_c=1, W=1, description="Wände und Angry Birds", minimum_length=19),
    Level(number=WINNER, name="Gewonnen", speed=100, normal_f_c=0, small_f_c=0, Angry_Bird_c=0, W=0, description="Du hast alle Level geschafft", minimum_length=20),
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
