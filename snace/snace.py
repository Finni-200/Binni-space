from kreise import Kreise
from essen import Essen
from klein_essen import KleinEssen
import random

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

OPPOSITE_DIRECTIONS = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


class Snace:

    def __init__(
        self,
        x_1,
        y,
        farbe,
        farbe_1,
        durchmesser,
        anzahl,
        wartezeit,
        spielfeld_width,
        spielfeld_height,
        spielrand,
        farbe_essen,
        durchmesser_essen,
    ):
        self.wartezeit = wartezeit
        self.durchmesser = durchmesser
        self.spielrand = spielrand
        self.length = anzahl

        self.spielfeld_width = spielfeld_width
        self.spielfeld_height = spielfeld_height

        self.min_x = spielrand + durchmesser / 2
        self.max_x = spielrand + spielfeld_width - durchmesser / 2
        self.min_y = spielrand + durchmesser / 2
        self.max_y = spielrand + spielfeld_height - durchmesser /2

        self.segments = []
        for index in range(anzahl):
            x = x_1 - index * durchmesser
            color = farbe_1 if index == 0 else farbe
            self.segments.append(Kreise(color, durchmesser, x, y))

        self.liste = self.segments
        self.anzahl = anzahl

        self.normal_essen = Essen(farbe_essen, durchmesser_essen, 0, 0)
        self.small_essen = KleinEssen("green", durchmesser_essen, 0, 0)

        self.essen = self.normal_essen
        self._spawn_food(self.normal_essen)
        self._spawn_food(self.small_essen, exclude={(self.normal_essen.x, self.normal_essen.y)})

        self.current_direction = None

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

    def move(self, direction):
        if direction in DIRECTION_VECTORS:
            if self.current_direction is None:
                self.current_direction = direction
            elif OPPOSITE_DIRECTIONS[self.current_direction] != direction:
                self.current_direction = direction

        if self.current_direction is None:
            return

        dx, dy = DIRECTION_VECTORS[self.current_direction]
        tail_position = (self.segments[-1].x, self.segments[-1].y)

        for index in range(self.length - 1, 0, -1):
            self.segments[index].x = self.segments[index - 1].x
            self.segments[index].y = self.segments[index - 1].y

        head = self.segments[0]
        head.x += dx * self.durchmesser
        head.y += dy * self.durchmesser

        if head.x < self.min_x:
            head.x = self.max_x
        elif head.x > self.max_x:
            head.x = self.min_x

        if head.y < self.min_y:
            head.y = self.max_y
        elif head.y > self.max_y:
            head.y = self.min_y

        if (head.x, head.y) == (self.normal_essen.x, self.normal_essen.y):
            old_position = (self.normal_essen.x, self.normal_essen.y)
            self.segments.append(Kreise(self.segments[-1].farbe, self.durchmesser, *tail_position))
            self.length = len(self.segments)
            self._spawn_food(
                self.normal_essen,
                exclude={old_position, (self.small_essen.x, self.small_essen.y)},
            )

        elif (head.x, head.y) == (self.small_essen.x, self.small_essen.y):
            old_position = (self.small_essen.x, self.small_essen.y)
            if self.length > 1:
                self.segments.pop()
                self.length = len(self.segments)
            self._spawn_food(
                self.small_essen,
                exclude={old_position, (self.normal_essen.x, self.normal_essen.y)},
            )

    def _shape_to_svg(self, shape):
        return {
            "cx": shape.x,
            "cy": shape.y,
            "r": shape.durchmesser / 2,
            "color": shape.farbe,
        }

    def get_kreise(self):
        return [self._shape_to_svg(segment) for segment in self.segments]

    def get_food_data(self):
        return [self._shape_to_svg(self.normal_essen)]

    def get_small_food_data(self):
        return [self._shape_to_svg(self.small_essen)]
