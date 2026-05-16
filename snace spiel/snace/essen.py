import random

class Essen:

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
    
    def berührt(self, körperteil):
        essen_x, essen_y = self.get_position()
        teil_x, teil_y = körperteil.get_position()

        if abs(essen_x - teil_x) < 50 and abs(essen_y - teil_y) < 50:
            return True
        return False