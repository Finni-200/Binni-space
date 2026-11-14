from dataclasses import dataclass
import math

@dataclass
class Spiel_Feld:
    breite : int
    höhe: int
    rand: int
    zellgrösse: int

    def update_field_size(self, breite, höhe) -> bool:
        radius = self.zellgrösse / 2
        self.min_x = self.rand + radius
        self.max_x = self.rand + breite - radius      
        self.min_y = self.rand + radius
        self.max_y = self.rand + höhe - radius


        neue_breite = max(
            self.zellgrösse,
            math.ceil((breite - self.rand * 2) / self.zellgrösse)
            * self.zellgrösse,
        )
        neue_hoehe = max(
            self.zellgrösse,
            math.floor((höhe - self.rand * 2) / self.zellgrösse)
            * self.zellgrösse,
        )
    
        geändert = (
            neue_breite != self.breite
            or neue_hoehe != self.hoehe
        )
    
        self.breite = neue_breite
        self.höhe = neue_hoehe
        return geändert


    def _shape_to_svg(shape):
        return {
            "cx": shape.x,
            "cy": shape.y,
            "r": shape.durchmesser / 2,
            "color": shape.farbe,
        }
    