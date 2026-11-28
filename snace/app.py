from flask import Flask, jsonify, render_template, request
from data import Data
from game import Game
from score_database import ScoreDatabase
from spiel_feld import Spiel_Feld
import threading
import time


app = Flask(__name__, template_folder="templates", static_folder="static")

LINE_COLOR = "#ff0000"
LINE_WIDTH = 4
SPIELRAND = 50
KREIS_DURCHMESSER = 50
FIELD_WIDTH = 1800
FIELD_HEIGHT = 950

spielfeld = Spiel_Feld(
    FIELD_WIDTH,
    FIELD_HEIGHT,
    SPIELRAND,
    KREIS_DURCHMESSER,
)
game = Game(spielfeld)
score_database = ScoreDatabase()
game_started = threading.Event()
game_lock = threading.Lock()
game_result = None


def move_snake_loop():
    while True:
        game_started.wait()
        with game_lock:
            result = game.tick()
            game_over = result["game_over"]
            delay = game.snake.wartezeit / 1000
        if game_over:
            finish_current_game()
        time.sleep(delay)


def move_angry_bird_loop():
    while True:
        game_started.wait()
        with game_lock:
            if game.game_over:
                game_over = True
            else:
                game_over = game.move_angry_bird()
        if game_over:
            finish_current_game()
        time.sleep(0.005)


@app.route("/")
def index():
    game_started.clear()
    return render_template(
        "index.html",
        **Data.get_index_data(game, spielfeld, score_database),
        line_color=LINE_COLOR,
        line_width=LINE_WIDTH,
    )


@app.route("/api/snake")
def api_snake():
    return jsonify(Data.get_game_data(game, game_result))


@app.route("/richtung/<richtung>")
def richtung(richtung):
    game.set_direction(richtung)
    return jsonify(Data.get_direction_data(game))


@app.route("/api/finish-game", methods=["POST"])
def finish_game():
    return jsonify(Data.get_finish_game_data(finish_current_game()))


def finish_current_game():
    global game_result

    with game_lock:
        if game_result is not None:
            return game_result
        if not game_started.is_set():
            return {"saved": False}

        game_started.clear()
        game_result = score_database.save_score(game.score)
        return game_result


@app.route("/api/start-game", methods=["POST"])
def start_game():
    global game, game_result

    with game_lock:
        game = Game(spielfeld)
        game_result = None
        game_started.set()
    return jsonify(Data.get_start_game_data(game))


@app.route("/update_field_size", methods=["POST"])
def update_field_size():
    data = request.get_json(silent=True) or {}
    width = data.get("width")
    height = data.get("height")

    if (
        isinstance(width, bool)
        or not isinstance(width, int)
        or isinstance(height, bool)
        or not isinstance(height, int)
    ):
        return jsonify({"error": "Ungültige Fenstergröße"}), 400

    with game_lock:
        game.update_field_size(width, height)

    return jsonify(Data.get_field_size_data(spielfeld))


if __name__ == "__main__":
    snake_thread = threading.Thread(target=move_snake_loop, daemon=True)
    angry_bird_thread = threading.Thread(
        target=move_angry_bird_loop,
        daemon=True,
    )
    snake_thread.start()
    angry_bird_thread.start()
    app.run(debug=True, use_reloader=False, port=5002)
