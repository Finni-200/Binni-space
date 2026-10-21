import random
from dataclasses import dataclass


@dataclass
class Angry_Bird:
    farbe: str
    durchmesser: int
    x: float
    y: float
    



def _spawn_angry_bird(self):
    occupied_positions = {
        (segment.x, segment.y) for segment in self.segments
    }
    occupied_positions.add((self.normal_essen.x, self.normal_essen.y))
    occupied_positions.add((self.small_essen.x, self.small_essen.y))

    x_steps = int((self.max_x - self.min_x) / self.durchmesser)
    y_steps = int((self.max_y - self.min_y) / self.durchmesser)
    while True:
        x = self.min_x + random.randint(0, x_steps) * self.durchmesser
        y = self.min_y + random.randint(0, y_steps) * self.durchmesser
        if (x, y) not in occupied_positions:
            self.angry_bird = {
                "color": "#2da44e",
                "r": self.durchmesser / 2,
                "cx": x,
                "cy": y,               
            }
            return


