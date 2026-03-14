from flask import Flask, render_template, request
from snace import körperteil
from essen import essen

app = Flask(__name__)

snace = körperteil("green", 50, 500, 500)
snace1 = körperteil("red", 50, 450, 500)
essen = essen("blue", 500, 500)


@app.route("/")
def index():

   return render_template(
        "index.html",
        farbe=snace.get_farbe(),
        durchmesser=snace.get_durchmesser(),
        x=snace.x,
        y=snace.y,

        farbe1=snace1.get_farbe(),
        durchmesser1=snace1.get_durchmesser(),
        x1=snace1.x,
        y1=snace1.y,

        essen_farbe=essen.get_farbe(),
        essen_x=essen.x,
        essen_y=essen.y

)

@app.route("/move")
def move():

    richtung = request.args.get("richtung")

    alt_x = snace.x
    alt_y = snace.y

    snace.bewegen(snace.get_durchmesser(), richtung)

    snace1.x = alt_x
    snace1.y = alt_y

    return {
        "x": snace.x,
        "y": snace.y,
        "x1": snace1.x,
        "y1": snace1.y
    }

if __name__ == "__main__":
    app.run(debug=True)