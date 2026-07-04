from flask import Flask, render_template, jsonify, request
from snace import Snace
import threading
import time

app = Flask(__name__, template_folder="templates", static_folder="static")

snake = Snace(
    x_1=950,
    y=450,
    farbe="red",
    farbe_1="green",
    durchmesser=50,
    anzahl=4,
    wartezeit=1000
)

current_direction = "right"


def move_snake_loop():
    while True:
        time.sleep(snake.wartezeit / 1000)
        snake.move(current_direction)


thread = threading.Thread(
    target=move_snake_loop,
    daemon=True
)
thread.start()


@app.route("/")
def index():
    return render_template("index.html", circles=snake.get_kreise())


@app.route("/api/snake")
def api_snake():
    return jsonify(snake.get_kreise())


@app.route("/richtung/<richtung>")
def richtung(richtung):

    global current_direction

    if richtung in ["up", "down", "left", "right"]:
        current_direction = richtung

    return jsonify({"richtung": current_direction})


@app.route("/fenster/<int:width>/<int:height>")
def fenster(width, height):
    snake.width = width
    snake.height = height
    return jsonify({"width": snake.width, "height": snake.height})


if __name__ == "__main__":
    app.run(debug=True)