from kreise import Kreise


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
        min_x=0,
        max_x=1800,
        min_y=0,
        max_y=950,
    ):
        self.wartezeit = wartezeit
        self.durchmesser = durchmesser
        self.length = anzahl
        self.score = 0
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.segments = []
        for index in range(anzahl):
            x = x_1 - index * durchmesser
            color = farbe_1 if index == 0 else farbe
            self.segments.append(Kreise(color, durchmesser, x, y))

        self.liste = self.segments
        self.anzahl = anzahl
        self.aktuelle_Richtung = None

    def get_kreise(self):
        return [
            {
                "cx": segment.x,
                "cy": segment.y,
                "r": segment.durchmesser / 2,
                "color": segment.farbe,
            }
            for segment in self.segments
        ]

    @staticmethod
    def create_snake(spielfeld, spielRand=None, Kreis_Durchmesser=None):
        diameter = Kreis_Durchmesser or spielfeld.zellgrösse
        margin = spielfeld.rand if spielRand is None else spielRand
        radius = diameter / 2
        min_x = margin + radius
        max_x = margin + spielfeld.breite - radius
        min_y = margin + radius
        max_y = margin + spielfeld.höhe - radius
        x_steps = max(0, int((max_x - min_x) // diameter))
        y_steps = max(0, int((max_y - min_y) // diameter))
        start_x = min_x + (x_steps // 2) * diameter
        start_y = min_y + (y_steps // 2) * diameter
        start_x = max(start_x, min_x + (3 * diameter))

        return Snace(
            x_1=start_x,
            y=start_y,
            farbe="red",
            farbe_1="green",
            durchmesser=diameter,
            anzahl=4,
            wartezeit=100,
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
        )

    def set_direction(self, direction):
        if direction not in DIRECTION_VECTORS:
            return
        if (
            self.aktuelle_Richtung is None
            or OPPOSITE_DIRECTIONS[self.aktuelle_Richtung] != direction
        ):
            self.aktuelle_Richtung = direction

    def move(self, direction=None, wrap=True):
        if direction is not None:
            self.set_direction(direction)
        if self.aktuelle_Richtung is None or not self.segments:
            return False

        dx, dy = DIRECTION_VECTORS[self.aktuelle_Richtung]
        head = self.segments[0]
        next_x = head.x + dx * self.durchmesser
        next_y = head.y + dy * self.durchmesser

        grid_min_x = self.min_x + (head.x - self.min_x) % self.durchmesser
        grid_min_y = self.min_y + (head.y - self.min_y) % self.durchmesser
        grid_max_x = grid_min_x + int(
            (self.max_x - grid_min_x) / self.durchmesser
        ) * self.durchmesser
        grid_max_y = grid_min_y + int(
            (self.max_y - grid_min_y) / self.durchmesser
        ) * self.durchmesser

        if next_x > grid_max_x or next_x < grid_min_x:
            if not wrap:
                return False
            next_x = grid_min_x if next_x > grid_max_x else grid_max_x
        if next_y > grid_max_y or next_y < grid_min_y:
            if not wrap:
                return False
            next_y = grid_min_y if next_y > grid_max_y else grid_max_y

        self.segments.insert(
            0,
            Kreise(head.farbe, self.durchmesser, next_x, next_y),
        )
        self.segments.pop()
        self.length = len(self.segments)
        self.anzahl = self.length
        self.liste = self.segments
        return True
