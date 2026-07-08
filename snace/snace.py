from kreise import Kreise


class Snace:

    def __init__(self, x_1, y, farbe, farbe_1, durchmesser, anzahl, wartezeit,width=1500,height=900):
        self.wartezeit = wartezeit
        self.durchmesser = durchmesser
        self.anzahl = anzahl
        self.width = width
        self.height = height

        # Erzeuge die Startliste der Kreise für die Schlange.
        self.liste = []
        for i in range(anzahl):
            x = x_1 - i * durchmesser
            color = farbe_1 if i == 0 else farbe
            self.liste.append(Kreise(color, durchmesser, x, y))

    


    def move(self, direction):

        for i in range(self.anzahl - 1, 0, -1):
            self.liste[i].x = self.liste[i - 1].x
            self.liste[i].y = self.liste[i - 1].y

        if direction == "up":
            self.liste[0].y -= self.durchmesser
        elif direction == "down":
            self.liste[0].y += self.durchmesser
        elif direction == "left":
            self.liste[0].x -= self.durchmesser
        elif direction == "right":
            self.liste[0].x += self.durchmesser

        if self.liste[0].x - 0.5 * self.durchmesser < self.durchmesser:
            self.liste[0].x = self.width - 0.5 * self.durchmesser
        elif self.liste[0].x + 0.5 * self.durchmesser > self.width - self.durchmesser:
            self.liste[0].x = 0.5 * self.durchmesser

        if self.liste[0].y - 0.5 * self.durchmesser < self.durchmesser:
            self.liste[0].y = self.height - 0.5 * self.durchmesser
        elif self.liste[0].y + 0.5 * self.durchmesser > self.height - self.durchmesser:
            self.liste[0].y = 0.5 * self.durchmesser
    
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