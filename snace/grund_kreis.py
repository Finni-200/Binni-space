from dataclasses import dataclass


@dataclass
class GrundKreis:
    """GrundKreis repräsentiert einen Kreis mit einem Mittelpunkt und einem Radius."""
    x: float  # X-Koordinate des Mittelpunkts
    y: float  # Y-Koordinate des Mittelpunkts
    durchmesser: int  # Durchmesser des Kreises
    farbe: str  # Farbe des Kreises

    @staticmethod
    def berechne_spielfeldgroesse(fenster_breite: int, fenster_hoehe: int, spielrand: int, durchmesser: int) -> tuple[int, int]:
        """Berechnet die sichtbare Spielfeldgröße aus der Fenstergröße.

        Das Ergebnis wird auf das nächstkleinere Vielfache des Durchmessers gerundet
        und berücksichtigt den Spielrand auf allen Seiten.
        """
        feld_breite = ((fenster_breite - spielrand * 2) // durchmesser) * durchmesser
        feld_hoehe = ((fenster_hoehe - spielrand * 2) // durchmesser) * durchmesser
        return feld_breite, feld_hoehe

    @staticmethod
    def berechne_zentrierte_position(feld_breite: int, feld_hoehe: int, spielrand: int) -> tuple[int, int]:
        """Berechnet die zentrale Position im Spielfeld mit dem gegebenen Rand."""
        x = spielrand + feld_breite // 2
        y = spielrand + feld_hoehe // 2
        return x, y
