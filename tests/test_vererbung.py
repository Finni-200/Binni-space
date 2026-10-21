import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from essen import Essen



class EssenVererbungTest(unittest.TestCase):
    def test_klein_essen_erbt_von_essen_und_behält_eigene_position(self):
        essen = Essen("green", 8, 12, 34)

        self.assertIsInstance(essen, Essen)
        self.assertEqual(essen.farbe, "green")
        self.assertEqual(essen.durchmesser, 8)
        self.assertEqual(essen.x, 12)
        self.assertEqual(essen.y, 34)


if __name__ == "__main__":
    unittest.main()
