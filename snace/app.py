from flask import Flask, render_template, request
from spieler import Spieler
from essen import Essen

app = Flask(__name__)

SPIEL_BREITE = 1200
SPIEL_HOEHE = 800

spieler1 = Spieler("Spieler 1", "pink", 600, 500, "right")
spieler2 = Spieler("Spieler 2", "cyan", 300, 200, "down")

essen_körper = Essen("blue", SPIEL_BREITE, SPIEL_HOEHE)


def get_kreise_für_render():
    return spieler1.get_segments() + spieler2.get_segments()


@app.route("/")
def index():
    return render_template(
        "index.html",
        kreise_für_render=get_kreise_für_render(),
        essen_farbe=essen_körper.get_farbe(),
        essen_x=essen_körper.x,
        essen_y=essen_körper.y,
    )


@app.route("/move")
def move():
    breite = int(request.args.get("breite"))
    hoehe = int(request.args.get("hoehe"))

    richtung1 = request.args.get("richtung1")
    richtung2 = request.args.get("richtung2")

    if richtung1:
        spieler1.set_richtung(richtung1)
    if richtung2:
        spieler2.set_richtung(richtung2)

    spieler1_ate = essen_körper.berührt(spieler1.get_kopf())
    spieler2_ate = essen_körper.berührt(spieler2.get_kopf())

    spieler1.bewege(breite, hoehe, wachse=spieler1_ate)
    spieler2.bewege(breite, hoehe, wachse=spieler2_ate)

    if spieler1.kollidiert_mit(spieler1.body[1:]) or spieler1.kollidiert_mit(spieler2.body):
        return {"status": "game over"}

    if spieler2.kollidiert_mit(spieler2.body[1:]) or spieler2.kollidiert_mit(spieler1.body):
        return {"status": "game over"}

    if spieler1_ate or spieler2_ate:
        essen_körper.bewege()

    return {
        "kreise": get_kreise_für_render(),
        "essen": {
            "x": essen_körper.x,
            "y": essen_körper.y,
        },
    }


if __name__ == "__main__":
    app.run(debug=True, port=5001)
