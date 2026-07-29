from kreise import Kreise
from essen import Essen
from klein_essen import KleinEssen
import random


class Snace:

    def __init__(self, x_1, y, farbe, farbe_1, durchmesser, anzahl, wartezeit, spielfeld_width, spielfeld_height, spielrand, farbe_essen, durchmesser_essen):
        self.wartezeit = wartezeit
        self.durchmesser = durchmesser
        self.anzahl = anzahl
        self.spielrand = spielrand

        # Spielfeldgröße (ohne Spielrand)
        self.spielfeld_width = spielfeld_width
        self.spielfeld_height = spielfeld_height
        
        # Absolute Grenzen (mit Spielrand)
        self.min_x = spielrand + durchmesser / 2
        self.max_x = spielrand + spielfeld_width - durchmesser / 2
        self.min_y = spielrand + durchmesser / 2
        self.max_y = spielrand + spielfeld_height - durchmesser / 2

        # Erzeuge die Startliste der Kreise
        self.liste = []
        for i in range(anzahl):
            x = x_1 - i * durchmesser
            color = farbe_1 if i == 0 else farbe
            self.liste.append(Kreise(color, durchmesser, x, y))

        # Erzeugt zwei verschiedene Essen-Objekte mit identischer Optik
        self.normal_essen = Essen(farbe_essen, durchmesser_essen, 0, 0)
        self.small_essen = KleinEssen(farbe_essen, durchmesser_essen, 0, 0)

        self.essen = self.normal_essen
        self._spawn_food(self.normal_essen)
        self._spawn_food(self.small_essen)

        self.current_direction = None

    def _spawn_food(self, food, other_food=None):
        x_steps = int(round((self.max_x - self.min_x) / self.durchmesser))
        y_steps = int(round((self.max_y - self.min_y) / self.durchmesser))

        occupied_positions = {(segment.x, segment.y) for segment in self.liste}
        if other_food is not None:
            occupied_positions.add((other_food.x, other_food.y))

        while True:
            x = self.min_x + random.randint(0, x_steps) * self.durchmesser
            y = self.min_y + random.randint(0, y_steps) * self.durchmesser

            if (x, y) not in occupied_positions:
                food.x = x
                food.y = y
                break

    def move(self, direction):
        if direction in ["up", "down", "left", "right"]:
            if self.current_direction is None:
                self.current_direction = direction
            elif (self.current_direction, direction) not in [
                ("up", "down"),
                ("down", "up"),
                ("left", "right"),
                ("right", "left"),
            ]:
                self.current_direction = direction

        if self.current_direction is None:
            return

        tail_x = self.liste[-1].x
        tail_y = self.liste[-1].y

        # Körper nachziehen
        for i in range(self.anzahl - 1, 0, -1):
            self.liste[i].x = self.liste[i - 1].x
            self.liste[i].y = self.liste[i - 1].y

        # Kopf bewegen
        if self.current_direction == "up":
            self.liste[0].y -= self.durchmesser
        elif self.current_direction == "down":
            self.liste[0].y += self.durchmesser
        elif self.current_direction == "left":
            self.liste[0].x -= self.durchmesser
        elif self.current_direction == "right":
            self.liste[0].x += self.durchmesser

        # Wandkollision mit Wrap-around
        # Linker / rechter Rand
        if self.liste[0].x < self.min_x:
            self.liste[0].x = self.max_x
        elif self.liste[0].x > self.max_x:
            self.liste[0].x = self.min_x

        # Oberer / unterer Rand
        if self.liste[0].y < self.min_y:
            self.liste[0].y = self.max_y
        elif self.liste[0].y > self.max_y:
            self.liste[0].y = self.min_y

        if self.liste[0].x == self.normal_essen.x and self.liste[0].y == self.normal_essen.y:
            self.anzahl += 1
            self.liste.append(Kreise(self.liste[-2].farbe, self.durchmesser, tail_x, tail_y))
            self._spawn_food(self.normal_essen, self.small_essen)

        if self.liste[0].x == self.small_essen.x and self.liste[0].y == self.small_essen.y:
            if len(self.liste) > 1:
                self.liste.pop()
                self.anzahl -= 1
            self._spawn_food(self.small_essen, self.normal_essen)

    def get_kreise(self):
        return [
            {
                "cx": kreis.x,
                "cy": kreis.y,
                "r": kreis.durchmesser / 2,
                "color": kreis.farbe
            }
            for kreis in self.liste
        ]

    def get_food_data(self):
        return [
            {
                "cx": self.normal_essen.x,
                "cy": self.normal_essen.y,
                "r": self.normal_essen.durchmesser / 2,
                "color": self.normal_essen.farbe,
            },
            {
                "cx": self.small_essen.x,
                "cy": self.small_essen.y,
                "r": self.small_essen.durchmesser / 2,
                "color": self.small_essen.farbe,
            },
        ]