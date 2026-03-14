import random
from flask import current_app as app
class Box:
    #eigenschaften
    def __init__(self,farbe,x_länge,y_breite):
        width = app.config.get("WIDTH", 800)
        height = app.config.get("HEIGHT", 600)
        self.farbe = farbe
        self.x_länge = x_länge
        self.y_breite = y_breite
        self.x = random.randint(0, width - self.x_länge)
        self.y = random.randint(0, height - self.y_breite) 
        
    #metode
    def bewege (self):
        width = app.config.get("WIDTH", 800)
        height = app.config.get("HEIGHT", 600)
        self.x = random.randint(0, width - self.x_länge)
        self.y = random.randint(0, height - self.y_breite)
    def get_position (self):
        return self.x,self.y
    def get_farbe (self) :
        return self.farbe