from flask import Flask, render_template,request
from box import Box

app = Flask(__name__)

@app.route("/")
def index():
    spiel_box = Box("red", 100, 100)
    x, y = spiel_box.get_position()

    return render_template(
        "index2.html",
        x=x,
        y=y,
        breite=spiel_box.x_länge,
        hoehe=spiel_box.y_breite,
        farbe=spiel_box.get_farbe()
    )

#@app.route("/fenster", methods=["POST"])
#def fenster():
#    data = request.json
#    app.config["WIDTH"] = data["width"]
#    app.config["HEIGHT"] = data["height"]
#    return "", 200

if __name__ == "__main__":
    app.run(debug=True)