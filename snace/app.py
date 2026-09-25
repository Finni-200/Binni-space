from flask import Flask, render_template, jsonify, request
from snace import Snace
from levels import get_level_for_length
import math
import threading
import time


app = Flask(__name__, template_folder="templates", static_folder="static")

LINE_COLOR = "#ff0000"
LINE_WIDTH = 4
SPIELRAND = 50
KREIS_DURCHMESSER = 50
ESSEN_DURCHMESSER = 50
FIELD_WIDTH = 1800
FIELD_HEIGHT = 950


def create_snake(width, height):
    start_x = SPIELRAND + (width // 2)
    start_y = SPIELRAND + (height // 2)

    return Snace(
        x_1=start_x,
        y=start_y,
        farbe="red",
        farbe_1="green",
        durchmesser=KREIS_DURCHMESSER,
        anzahl=4,
        wartezeit=100,
        spielfeld_width=width,
        spielfeld_height=height,
        spielrand=SPIELRAND,
        farbe_essen="blue",
        durchmesser_essen=ESSEN_DURCHMESSER,
    )


snake = create_snake(FIELD_WIDTH, FIELD_HEIGHT)
current_direction = "right"


def move_snake_loop():
    global current_direction

    while True:
        snake.move(current_direction)
        time.sleep(snake.wartezeit / 1000)


@app.route("/")
def index():
    return render_template(
        "index.html",
        circles=snake.get_kreise(),
        foods=snake.get_food_data(),
        small_foods=snake.get_small_food_data(),
        angry_birds=snake.get_angry_bird_data(),
        spielrand=SPIELRAND,
        line_color=LINE_COLOR,
        line_width=LINE_WIDTH,
        current_level=get_level_for_length(snake.length).number,
    )


@app.route("/api/snake")
def api_snake():
    return jsonify(
        snake=snake.get_kreise(),
        foods=snake.get_food_data(),
        small_foods=snake.get_small_food_data(),
        angry_birds=snake.get_angry_bird_data(),
        current_level=get_level_for_length(snake.length).number,
    )


@app.route("/richtung/<richtung>")
def richtung(richtung):
    global current_direction

    if richtung in ["up", "down", "left", "right"]:
        current_direction = richtung

    return jsonify({"richtung": current_direction})


@app.route("/update_field_size", methods=["POST"])
def update_field_size():
    global FIELD_WIDTH, FIELD_HEIGHT, snake

    data = request.json or {}
    width = data.get("width")
    height = data.get("height")

    if isinstance(width, int) and isinstance(height, int):
        new_width = math.ceil((width - SPIELRAND * 2) / KREIS_DURCHMESSER) * KREIS_DURCHMESSER
        new_height = math.floor((height - SPIELRAND * 2) / KREIS_DURCHMESSER) * KREIS_DURCHMESSER

        if new_width != FIELD_WIDTH or new_height != FIELD_HEIGHT:
            FIELD_WIDTH = new_width
            FIELD_HEIGHT = new_height
            snake = create_snake(FIELD_WIDTH, FIELD_HEIGHT)

    return jsonify(field_width=FIELD_WIDTH, field_height=FIELD_HEIGHT)


if __name__ == "__main__":
    thread = threading.Thread(target=move_snake_loop, daemon=True)
    thread.start()
    app.run(debug=True, use_reloader=False, port=5001)
    