from dataclasses import dataclass
import math
import random


@dataclass
class Angry_Bird:
    farbe: str
    durchmesser: int
    x: float
    y: float
    direction_x: float = math.sqrt(0.5)
    direction_y: float = math.sqrt(0.5)

    def move(self, min_x, max_x, min_y, max_y, distance):
        next_x = self.x + self.direction_x * distance
        next_y = self.y + self.direction_y * distance

        hit_x = next_x < min_x or next_x > max_x
        hit_y = next_y < min_y or next_y > max_y
        if not hit_x and not hit_y:
            self.x = next_x
            self.y = next_y
            return

        if next_x < min_x:
            next_x = min_x
            inward_x = 1
        elif next_x > max_x:
            next_x = max_x
            inward_x = -1
        else:
            inward_x = 0

        if next_y < min_y:
            next_y = min_y
            inward_y = 1
        elif next_y > max_y:
            next_y = max_y
            inward_y = -1
        else:
            inward_y = 0

        reflected_x = -self.direction_x if hit_x else self.direction_x
        reflected_y = -self.direction_y if hit_y else self.direction_y
        max_turn = 90
        if hit_x:
            incidence = math.degrees(
                math.atan2(abs(self.direction_y), abs(self.direction_x))
            )
            max_turn = min(max_turn, 90 - incidence)
        if hit_y:
            incidence = math.degrees(
                math.atan2(abs(self.direction_x), abs(self.direction_y))
            )
            max_turn = min(max_turn, 90 - incidence)

        max_turn = max(0, max_turn - 0.001)
        turn = math.radians(random.uniform(min(2, max_turn), max_turn))
        turn *= random.choice((-1, 1))
        cosine = math.cos(turn)
        sine = math.sin(turn)
        direction_x = reflected_x * cosine - reflected_y * sine
        direction_y = reflected_x * sine + reflected_y * cosine

        if hit_x:
            direction_x = inward_x * abs(direction_x)
        if hit_y:
            direction_y = inward_y * abs(direction_y)
        length = math.hypot(direction_x, direction_y)

        self.x = next_x
        self.y = next_y
        self.direction_x = direction_x / length
        self.direction_y = direction_y / length
