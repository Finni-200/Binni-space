import random
class Box:
    #eigenschaften
    def __init__(self,farbe,x_länge,y_breite):
        self.x = random.randint (0, 1000)
        self.y = random.randint (0, 1000)
        self.farbe = farbe
        self.x_länge = x_länge
        self.y_breite = y_breite
        
    #metode
    def bewege (self):
        self.x = random.randint (0, 1000)
        self.y = random.randint (0, 1000)
    def get_posizion (self):
        return self.x,self.y