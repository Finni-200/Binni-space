from flask import Flask, render_template, jsonify, request
from snace import Snace
from kreise import Kreise
from essen import Essen
import threading
import time



app = Flask(__name__, template_folder="templates", static_folder="static")

LINE_COLOR = "#ff0000"
LINE_WIDTH = 4
SPIELRAND = 50
DURCHMESSER = 50

# Globale Variablen für dynamische Größe
FIELD_WIDTH = 1800
FIELD_HEIGHT = 950
START_X = SPIELRAND + (FIELD_WIDTH // 2)
START_Y = SPIELRAND + (FIELD_HEIGHT // 2)

snake = Snace(
    x_1=START_X,
    y=START_Y,
    farbe="red",
    farbe_1="green",
    durchmesser=DURCHMESSER,
    anzahl=4,
    wartezeit=100,
    spielfeld_width=FIELD_WIDTH,
    spielfeld_height=FIELD_HEIGHT,
    spielrand=SPIELRAND,
    farbe_essen="blue",
    durchmesser_essen=25,
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
        foods=snake.get_food_data(),
        small_foods=snake.get_small_food_data(),
        spielrand=SPIELRAND,
        line_color=LINE_COLOR,
        line_width=LINE_WIDTH,
    )

@app.route("/api/snake")
def api_snake():
    return jsonify({
        "snake": snake.get_kreise(),
        "foods": snake.get_food_data(),
        "small_foods": snake.get_small_food_data(),
    })


@app.route("/richtung/<richtung>")
def richtung(richtung):
    global current_direction

    if richtung in ["up", "down", "left", "right"]:
        current_direction = richtung

    return jsonify({"richtung": current_direction})


@app.route("/update_field_size", methods=["POST"])
def update_field_size():
    global FIELD_WIDTH, FIELD_HEIGHT, START_X, START_Y, snake
    
    data = request.json
    width = data.get("width")
    height = data.get("height")
    
    if width and height:
        # Berechne neue Spielfeldgröße
        new_width = ((width - SPIELRAND * 2) // DURCHMESSER) * DURCHMESSER
        new_height = ((height - SPIELRAND * 2) // DURCHMESSER) * DURCHMESSER
        
        # Nur wenn sich die Größe geändert hat, Schlange neu initialisieren
        if new_width != FIELD_WIDTH or new_height != FIELD_HEIGHT:
            FIELD_WIDTH = new_width
            FIELD_HEIGHT = new_height
            START_X = SPIELRAND + (FIELD_WIDTH // 2) - (DURCHMESSER // 2)
            START_Y = SPIELRAND + (FIELD_HEIGHT // 2) - (DURCHMESSER // 2)
            
            # Reinitialize snake with new dimensions
            snake = Snace(
                x_1=START_X,
                y=START_Y,
                farbe="red",
                farbe_1="green",
                durchmesser=DURCHMESSER,
                anzahl=4,
                wartezeit=100,
                spielfeld_width=FIELD_WIDTH,
                spielfeld_height=FIELD_HEIGHT,
                spielrand=SPIELRAND,
                farbe_essen="blue",
                durchmesser_essen=50,
            )
    
    return jsonify({
        "field_width": FIELD_WIDTH,
        "field_height": FIELD_HEIGHT
    })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)
    