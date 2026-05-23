from segment import körperteil



class Spieler:

    OPPOSITE_DIRECTIONS = {
        "up": "down",
        "down": "up",
        "left": "right",
        "right": "left",
    }


    def __init__(self, name, farbe, start_x, start_y, start_richtung="right"):
        self.name = name
        self.farbe = farbe
        self.durchmesser = 50
        self.richtung = start_richtung
        # Body enthält die Segmente; Kopf ist Index 0
        self.body = [
            körperteil(farbe, self.durchmesser, start_x, start_y),
            körperteil(farbe, self.durchmesser, start_x - self.durchmesser, start_y),
        ]

    # Richtung ändern: ignoriert ungültige Richtungen und sofortige Gegenrichtung
    def set_richtung(self, neue_richtung):
        if neue_richtung not in self.OPPOSITE_DIRECTIONS:
            return
        # Verhindert direkte Drehung um 180° (selbstkollision)
        if self.OPPOSITE_DIRECTIONS[neue_richtung] == self.richtung:
            return
        self.richtung = neue_richtung


    def get_kopf(self):
        return self.body[0]

    # Bewegung der Schlange: berechnet neuen Kopf, bewegt Segmente, optionales Wachsen
    def bewege(self, breite, hoehe, wachse=False):
        kopf = self.get_kopf()
        d = self.durchmesser
        neuer_x = kopf.x
        neuer_y = kopf.y


        if self.richtung == "right":
            neuer_x += d
        elif self.richtung == "left":
            neuer_x -= d
        elif self.richtung == "up":
            neuer_y -= d
        elif self.richtung == "down":
            neuer_y += d

        # Bildschirmränder: Wrap-Around (kommt auf gegenüberliegende Seite)
        if neuer_x >= breite:
            neuer_x = 0
        elif neuer_x < 0:
            neuer_x = breite - d

        if neuer_y >= hoehe:
            neuer_y = 0
        elif neuer_y < 0:
            neuer_y = hoehe - d

        alt_x = kopf.x
        alt_y = kopf.y


        kopf.x = neuer_x
        kopf.y = neuer_y

        # Jedes Segment nimmt die Position des vorherigen Segments an
        for segment in self.body[1:]:
            temp_x = segment.x
            temp_y = segment.y
            segment.x = alt_x
            segment.y = alt_y
            alt_x = temp_x
            alt_y = temp_y


        if wachse:
            self.body.append(körperteil(self.farbe, d, alt_x, alt_y))

    # Prüft, ob der Kopf mit einer Liste von Teilen kollidiert 
    def kollidiert_mit(self, teile):
        kopf = self.get_kopf()
        for teil in teile:
            if kopf.x == teil.x and kopf.y == teil.y:
                return True
        return False

    
    def get_segments(self):
        return [
            {
                "x": teil.x,
                "y": teil.y,
                "farbe": teil.farbe,
                "durchmesser": teil.get_durchmesser(),
            }
            for teil in self.body
        ]
