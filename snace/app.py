from flask import Flask, render_template
from snace import Snace


# Konfiguration der Schlange
x_1 = 300
y = 0
farbe = "red"
farbe_1 = "black"
durchmesser = 50
anzahl = 3
speed = 100 


def speed():
    snace 'speed' = 100
    return _speed_value

app = Flask(__name__, static_folder="static", template_folder="temlates")


@app.route("/")
def index():
    current_speed = speed()
    snake = Snace(x_1, y, farbe, farbe_1, durchmesser, anzahl, current_speed)
    circles = [
        {
            "cx": c.x,
            "cy": c.y + 100,
            "r": c.durchmesser / 2,
            "color": c.farbe,
        }
        for c in snake.liste
    ]
    snake_data = {
        "speed": snake.speed(),
        "durchmesser": durchmesser,
        "anzahl": anzahl,
    }
    return render_template("index.html", circles=circles, snake_data=snake_data)
    



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)