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
        # Bewegt die Schlange in die angegebene Richtung.
        self.direction = direction
        if self.direction == 'right':
            for kreis in self.liste:
                kreis.x += 50

        if self.direction == 'left':
            for kreis in self.liste:
                kreis.x -= 50

        if self.direction == 'up':
            for kreis in self.liste:
                kreis.y -= 50

        if self.direction == 'down':
            for kreis in self.liste:
                kreis.y += 50

    
    
    if self.direction == 'right':
    for kreis in self.liste:
        kreis.x += 50

    if self.direction == 'left':
    for kreis in self.liste:
        kreis.x -= 50
  
    if self.direction == 'up':
    for kreis in self.liste:
        kreis.y += 50

    if self.direction == 'down':
    for kreis in self.liste:
        kreis.y -= 50



    def wand_kolision(self):
        # Überprüft, ob der Kopf mit dem rand des bilsdschirms kollidiert.
        kopf = self.liste[0]
        if kopf.x < 0 or kopf.x > 1000 or kopf.y < 0 or kopf.y > 1000:
            return True
        return False

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