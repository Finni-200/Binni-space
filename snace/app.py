from flask import Flask, render_template, jsonify
from snace import Snace
import threading
import time


app = Flask(__name__, template_folder="temlates", static_folder="static")

# Globale Konfiguration der Schlange.
# Hier kannst du Werte wie speed direkt in app.py sehen und ändern.
snake = Snace(
    x_1=500,
    y=500,
    farbe="red",
    farbe_1="green",
    durchmesser=50,
    anzahl=4,
    wartezeit=100
)


def move_snake_loop():
    #Bewegt die Schlange im Hintergrund alle x Millisekunden
    while True:
        time.sleep(snake.wartezeit / 1000)
        snake.move()


thread = threading.Thread(
    target=move_snake_loop,
    daemon=True
)
thread.start()


@app.route("/")
def index():

    snake_data = {
        "speed": snake.wartezeit,
        "diameter": snake.durchmesser,
        "count": len(snake.liste),
    }
    circles = snake.get_kreise()
    return render_template("index.html", circles=circles, snake_data=snake_data)


@app.route("/api/snake")
def api_snake():
    # Liefert die aktuellen Positionen der Kreise als JSON für das Frontend.
    return jsonify(snake.get_kreise())


if __name__ == "__main__":
    app.run(debug=True)