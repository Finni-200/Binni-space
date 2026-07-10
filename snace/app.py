from flask import Flask, render_template, jsonify, request
from snace import Snace
import threading
import time

app = Flask(__name__, template_folder="templates", static_folder="static")

LINE_COLOR = "#ff0000"
LINE_WIDTH = 4
SPIELRAND = 50

snake = Snace(
    x_1=100,
    y=100,
    farbe="red",
    farbe_1="green",
    durchmesser=50,
    anzahl=4,
    wartezeit=1000,

)

current_direction = "right"


def move_snake_loop():
    global current_direction

    while True:
        snake.move(current_direction)
        time.sleep(snake.wartezeit / 1000)


thread = threading.Thread(target=move_snake_loop, daemon=True)
thread.start()


@app.route("/")
def index():
    return render_template(
        "index.html",
        circles=snake.get_kreise(),
        spielrand=SPIELRAND,
        line_color=LINE_COLOR,
        line_width=LINE_WIDTH,
    )

@app.route("/api/snake")
def api_snake():
    return jsonify(snake.get_kreise())


@app.route("/richtung/<richtung>")
def richtung(richtung):
    global current_direction

    if richtung in ["up", "down", "left", "right"]:
        current_direction = richtung

    return jsonify({"richtung": current_direction})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)