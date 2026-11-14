from dataclasses import dataclass

from kreise import Kreise


@dataclass
class Essen(Kreise):
    farbe: str = "green"
    durchmesser: int = 50
    x: float = 0
    y: float = 0
