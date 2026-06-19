from kreise import Kreise


class Snace:

    def __init__(self, x_1, y, farbe, farbe_1, durchmesser, anzahl, speed):
        self._speed = speed
        self.durchmesser = durchmesser

        # Erzeuge die Startliste der Kreise für die Schlange.
        self.liste = []
        for i in range(anzahl):
            x = x_1 - i * durchmesser
            color = farbe_1 if i == 0 else farbe
            self.liste.append(Kreise(color, durchmesser, x, y))

    def speed(self):
        # Liefert den Wert für das Animationstempo zurück.
        return self._speed

    def move(self):
        # Bewege den Kopf und lasse den Körper nachziehen.
        kopf = self.liste[0]

        alt_x = kopf.x
        alt_y = kopf.y

        # Kopf um einen Kreis nach rechts verschieben.
        kopf.x += self.durchmesser

        # Körpersegmente folgen der alten Position des vorherigen Segments.
        for i in range(1, len(self.liste)):
            temp_x = self.liste[i].x
            temp_y = self.liste[i].y

            self.liste[i].x = alt_x
            self.liste[i].y = alt_y

            alt_x = temp_x
            alt_y = temp_y

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