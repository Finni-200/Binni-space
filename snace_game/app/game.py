from player import Spieler
from food import Essen

class Game:
    """Main game class managing game logic"""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.spieler1 = Spieler("Spieler 1", (255, 0, 0), 100, 100)
        self.spieler2 = Spieler("Spieler 2", (0, 0, 255), 700, 500, "left")
        self.essen = Essen((0, 255, 0), width, height)
    
    def get_game_state(self):
        """Return current game state"""
        return {
            'spieler1': {
                'body': [(s.x, s.y) for s in self.spieler1.body],
                'farbe': self.spieler1.farbe
            },
            'spieler2': {
                'body': [(s.x, s.y) for s in self.spieler2.body],
                'farbe': self.spieler2.farbe
            },
            'essen': {
                'x': self.essen.x,
                'y': self.essen.y,
                'farbe': self.essen.farbe
            }
        }
    
    def update(self):
        """Update game state"""
        self.spieler1.bewege(self.width, self.height)
        self.spieler2.bewege(self.width, self.height)
