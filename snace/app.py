from flask import Flask, render_template, jsonify, request
from snace import Snace
import threading
import time

app = Flask(__name__, template_folder="templates", static_folder="static")

# Einfach änderbare Werte für das Spielfeld
MARGIN_LEFT = 50
MARGIN_TOP = 50
MARGIN_RIGHT = 50
MARGIN_BOTTOM = 50
FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
LINE_COLOR = "#ff0000"
LINE_WIDTH = 4

snake = Snace(
    x_1=100,
    y=100,
    farbe="red",
    farbe_1="green",
    durchmesser=50,
    anzahl=4,
    wartezeit=1000,
    width=FIELD_WIDTH,
    height=FIELD_HEIGHT
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
    return render_template(
        "index.html",
        circles=snake.get_kreise(),
        margin_left=MARGIN_LEFT,
        margin_top=MARGIN_TOP,
        margin_right=MARGIN_RIGHT,
        margin_bottom=MARGIN_BOTTOM,
        field_width=FIELD_WIDTH,
        field_height=FIELD_HEIGHT,
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


@app.route("/fenster/<int:width>/<int:height>")
def fenster(width, height):
    snake.width = width
    snake.height = height
    return jsonify({"width": snake.width, "height": snake.height})


if __name__ == "__main__":
    app.run(debug=True)