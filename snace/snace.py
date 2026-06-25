from kreise import Kreise


class Snace:

    def __init__(self, x_1, y, farbe, farbe_1, durchmesser, anzahl, wartezeit):
        self.wartezeit = wartezeit
        self.durchmesser = durchmesser

        # Erzeuge die Startliste der Kreise für die Schlange.
        self.liste = []
        for i in range(anzahl):
            x = x_1 - i * durchmesser
            color = farbe_1 if i == 0 else farbe
            self.liste.append(Kreise(color, durchmesser, x, y))

    


    def move(self, direction):

        kreis.x = self.liste[0].x
        kreis.y = self.liste[0].y
    
        for kreis in self.liste:
    
            if direction == "right":
                kreis.x += 50
    
            elif direction == "left":
                kreis.x -= 50
    
            elif direction == "up":
                kreis.y -= 50
    
            elif direction == "down":
                kreis.y += 50

    
    def get_kreise(self):
        # Wandelt die Liste der Kreis-Objekte in einfache Dictionary-Daten um.
        return [
            {
                "cx": kreis.x,
                "cy": kreis.y,
                "r": kreis.durchmesser / 2,
                "color": kreis.farbe
            }
            for kreis in self.liste
        ]