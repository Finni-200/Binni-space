from flask import Flask, render_template, request
from ich import ich

app = Flask(__name__)

ich = ich("red", 50, 500, 500)



@app.route("/")
def index():

   return render_template(
        "index.html",
        farbe=ich.get_farbe(),
        durchmesser=ich.get_durchmesser(),
        x=ich.x,
        y=ich.y
   )

@app.route("/move")
def move():

    richtung = request.args.get("richtung")

    ich.bewegen(ich.get_durchmesser(), richtung)

    return {
        "x": ich.x,
        "y": ich.y
    }

if __name__ == "__main__":
    app.run(debug=True)