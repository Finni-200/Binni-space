from kreise import Kreise

class Snace:
    def __init__(self, x_1, y, farbe, farbe_1, durchmesser, anzahl, speed):
        self._speed = speed
        self.liste = []

        for i in range(anzahl):
            x = x_1 - i * durchmesser
            color = farbe_1 if i == 0 else farbe
            self.liste.append(Kreise(color, durchmesser, x, y))

    def speed(self):
        """Return the snake animation speed in milliseconds."""
        return self._speed