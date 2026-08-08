import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from grund_kreis import GrundKreis


def test_berechne_spielfeldgroesse_rundet_auf_vielfaches_von_durchmesser():
    feld_breite, feld_hoehe = GrundKreis.berechne_spielfeldgroesse(
        fenster_breite=1825,
        fenster_hoehe=975,
        spielrand=50,
        durchmesser=50,
    )

    assert feld_breite == 1750
    assert feld_hoehe == 850


def test_berechne_zentrierte_position_rechnet_mittelpunkt_mit_rand():
    x, y = GrundKreis.berechne_zentrierte_position(
        feld_breite=1750,
        feld_hoehe=850,
        spielrand=50,
    )

    assert x == 50 + 1750 // 2
    assert y == 50 + 850 // 2
