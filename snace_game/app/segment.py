
class körperteil:

    def __init__(self, farbe, durchmesser, x, y):
        self.farbe = farbe
        self.durchmesser = durchmesser
        self.x = x
        self.y = y
    
    def bewegen(self,durchmesser, richtung):
        if richtung == "up":
            self.y -= durchmesser
        elif richtung == "down":
            self.y += durchmesser
        elif richtung == "left":
            self.x -= durchmesser
        elif richtung == "right":
            self.x += durchmesser
       

    def get_durchmesser(self):
        return self.durchmesser

    def get_farbe(self):
        return self.farbe
    
    def get_position(self):
        return self.x, self.y