import random

class essen:

    def __init__(self, farbe, x_länge, y_länge):
        self.farbe = farbe
        self.x_länge = x_länge
        self.y_länge = y_länge
        self.x = random.randint(0, x_länge - 10)
        self.y = random.randint(0, y_länge - 10)

    # methode
    def bewege(self):
        self.x = random.randint(0, self.x_länge - 10)
        self.y = random.randint(0, self.y_länge - 10)

    def get_position(self):
        return self.x, self.y

    def get_farbe(self):
        return self.farbe