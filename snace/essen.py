
class Essen:
    def __init__(self, farbe_essen, durchmesser_essen, x_essen, y_essen):
        self.farbe = farbe_essen
        self.durchmesser = durchmesser_essen
        self.x = x_essen
        self.y = y_essen

    def beschreibe(self):
        return f"Essen: Farbe={self.farbe}, Durchmesser={self.durchmesser}"