from kreise import Kreise
from angry_bird import Angry_Bird
from essen import Essen
from levels import get_level, get_level_for_length, get_next_level
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
        self.score = 0

        self.spielfeld_width = spielfeld_width
        self.spielfeld_height = spielfeld_height

        radius = durchmesser / 2

        self.min_x = spielrand + radius
        self.max_x = spielrand + spielfeld_width - radius      
        self.min_y = spielrand + radius
        self.max_y = spielrand + spielfeld_height - radius

        self.segments = []
        for index in range(anzahl):
            x = x_1 - index * durchmesser
            color = farbe_1 if index == 0 else farbe
            self.segments.append(Kreise(color, durchmesser, x, y))

        self.liste = self.segments
        self.anzahl = anzahl

        self.normal_essen = Essen(farbe_essen, durchmesser_essen, 0, 0)
        self.small_essen = Essen("green", durchmesser_essen, 0, 0)
        self.angry_bird = Angry_Bird("green", 50, x, y)

        self.essen = self.normal_essen
        self._spawn_food(self.normal_essen)
        if get_level_for_length(self.length).number >= 2:
            self._spawn_food(self.small_essen, exclude={(self.normal_essen.x, self.normal_essen.y)})

        self.aktuelle_Richtung = None
        self.current_level = get_level(1)
        self.food_eaten_in_level = 0
        self.required_food_for_level = 2

    def direction(self, direction):
        if direction in DIRECTION_VECTORS:
                    if self.aktuelle_Richtung is None:
                        self.aktuelle_Richtung = direction
                    elif OPPOSITE_DIRECTIONS[self.aktuelle_Richtung] != direction:
                        self.aktuelle_Richtung = direction
        
                    if self.aktuelle_Richtung is None:
                        return {"ate_normal_food": False, "level_up": False}
        


    def move(self):

        if get_level_for_length(self.length).number >= 2 and self.small_essen.x == 0 and self.small_essen.y == 0:
            self._spawn_food(self.small_essen, exclude={(self.normal_essen.x, self.normal_essen.y)})

        dx, dy = DIRECTION_VECTORS[self.aktuelle_Richtung]
        tail_position = (self.segments[-1].x, self.segments[-1].y)


        if get_level_for_length(self.length).Angry_Bird_c:
            if self.angry_bird is None:
                self._spawn_angry_bird()

        ate_normal_food = False
        level_up = False

        if (head.x, head.y) == (self.normal_essen.x, self.normal_essen.y):
            old_position = (self.normal_essen.x, self.normal_essen.y)
            self.segments.append(Kreise(self.segments[-1].farbe, self.durchmesser, *tail_position))
            self.length = len(self.segments)
            self.food_eaten_in_level += 1
            self.score += 1
            ate_normal_food = True
            self._spawn_food(
                self.normal_essen,
                exclude={old_position, (self.small_essen.x, self.small_essen.y)},
            )

        elif get_level_for_length(self.length).number >= 2 and (head.x, head.y) == (self.small_essen.x, self.small_essen.y):
            old_position = (self.small_essen.x, self.small_essen.y)
            if self.length > 1:
                self.segments.pop()
                self.length = len(self.segments)
            self._spawn_food(
                self.small_essen,
                exclude={old_position, (self.normal_essen.x, self.normal_essen.y)},
            )

        if ate_normal_food and self.food_eaten_in_level >= self.required_food_for_level:
            next_level = get_next_level(self.current_level.number)
            if next_level is not None:
                self.current_level = next_level
                self.wartezeit = next_level.speed
                self.food_eaten_in_level = 0
                level_up = True

        return {"ate_normal_food": ate_normal_food, "level_up": level_up}

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
        if get_level_for_length(self.length).number < 2:
            return []
        return [self._shape_to_svg(self.small_essen)]

    def get_angry_bird_data(self):
        level = get_level_for_length(self.length)
        if level.Angry_Bird_c == 0:
            return []
        if self.angry_bird is None:
            self._spawn_angry_bird()
        return [self.angry_bird]
