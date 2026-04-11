from flask import Flask, render_template, request
from snace import körperteil
from essen import Essen

app = Flask(__name__)

SPIEL_BREITE = 1200
SPIEL_HOEHE = 800

global akuelle_richtung
akuelle_richtung = "right"

kreise = []


kreise.append(körperteil("pink", 50, 600, 500))
kreise.append(körperteil("pink", 50, 550, 500))


essen_körper = Essen("blue", 500, 500)
kreise_für_render = []
for teil in kreise:
    kreise_für_render.append({
        "farbe": teil.farbe,
        "x": teil.x,
        "y": teil.y,
        "durchmesser": teil.get_durchmesser()
    })

@app.route("/") 
def index(): 

    return render_template(
         "index.html",

          kreise_für_render=kreise_für_render,

          essen_farbe=essen_körper.get_farbe(), 
          essen_x=essen_körper.x, 
          essen_y=essen_körper.y )

@app.route("/move")
def move():

    breite = int(request.args.get("breite"))
    hoehe = int(request.args.get("hoehe"))

    global akuelle_richtung

    richtung = request.args.get("richtung")


    if akuelle_richtung == "right":
        if richtung == "left":
            return {"status": "invalid"}

    if akuelle_richtung == "left":
        if richtung == "right":
            return {"status": "invalid"}

    if akuelle_richtung == "up":
        if richtung == "down":
            return {"status": "invalid"}

    if akuelle_richtung == "down":
        if richtung == "up":
            return {"status": "invalid"}

    akuelle_richtung = richtung

    kopf = kreise[0]
    d = kopf.get_durchmesser()

    neuer_x = kopf.x
    neuer_y = kopf.y

    if richtung == "right":
        neuer_x += d
    elif richtung == "left":
        neuer_x -= d

    elif richtung == "up":
        neuer_y -= d
    elif richtung == "down":
        neuer_y += d

    if neuer_x >= breite:
        neuer_x = 0
    elif neuer_x < 0:
        neuer_x = breite - d
    
    if neuer_y >= hoehe:
        neuer_y = 0
    elif neuer_y < 0:
        neuer_y = hoehe - d

    berührt_prüfung = essen_körper.berührt(kopf)

 
    if berührt_prüfung:
        zu_prüfen = kreise
    else:
        zu_prüfen = kreise[:-1]

    for teil in zu_prüfen:
        if neuer_x == teil.x and neuer_y == teil.y:
            return {"status": "game over"}


    alt_x = kopf.x
    alt_y = kopf.y

    kopf.x = neuer_x
    kopf.y = neuer_y

    for i in range(1, len(kreise)):
        temp_x = kreise[i].x
        temp_y = kreise[i].y

        kreise[i].x = alt_x
        kreise[i].y = alt_y

        alt_x = temp_x
        alt_y = temp_y


    letzter_kreis = kreise[-1]
    vorletzter_kreis = kreise[-2]

    letzter_x = letzter_kreis.x
    letzter_y = letzter_kreis.y

    vorletzter_x = vorletzter_kreis.x
    vorletzter_y = vorletzter_kreis.y


    berührt_prüfung = essen_körper.berührt(kreise[0])

    if berührt_prüfung:

        essen_körper.bewege()

        if letzter_x == vorletzter_x and letzter_y < vorletzter_y:
            kreise.append(körperteil("pink", 50, letzter_x, letzter_y - letzter_kreis.get_durchmesser())) 

        elif letzter_x == vorletzter_x and letzter_y > vorletzter_y:
            kreise.append(körperteil("pink", 50, vorletzter_x, vorletzter_y + vorletzter_kreis.get_durchmesser()))

        elif letzter_y == vorletzter_y and letzter_x < vorletzter_x:
            kreise.append(körperteil("pink", 50, vorletzter_x - vorletzter_kreis.get_durchmesser(), vorletzter_y))

        elif letzter_y == vorletzter_y and letzter_x > vorletzter_x:
            kreise.append(körperteil("pink", 50, vorletzter_x + vorletzter_kreis.get_durchmesser(), vorletzter_y))

    return {
        "kreise": [
            {"x": teil.x, "y": teil.y}
            for teil in kreise
        ],
        "essen": {
            "x": essen_körper.x,
            "y": essen_körper.y
        }
    }



if __name__ == "__main__":
    app.run(debug=True, port=5001)
