from dataclasses import dataclass
import random


@dataclass
class Essen:
    farbe: str
    durchmesser: int
    x: float
    y: float


    def _spawn_food(self, food, exclude=None):
            x_steps = int((self.max_x - self.min_x) / self.durchmesser)
            y_steps = int((self.max_y - self.min_y) / self.durchmesser)
    
            occupied_positions = {(segment.x, segment.y) for segment in self.segments}
            if exclude is not None:
                occupied_positions |= exclude
    
            while True:
                x = self.min_x + random.randint(0, x_steps) * self.durchmesser
                y = self.min_y + random.randint(0, y_steps) * self.durchmesser
    
                if (x, y) not in occupied_positions:
                    food.x = x
                    food.y = y
                    return
       