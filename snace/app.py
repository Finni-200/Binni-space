from flask import Flask, render_template, request

from flask_socketio import SocketIO, emit

import threading
import time

from snace import körperteil
from spieler import Spieler
from essen import Essen

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

SPIEL_BREITE = 1200
SPIEL_HOEHE = 800

spieler1 = Spieler("Spieler 1", "pink", 600, 500, "right")
spieler2 = Spieler("Spieler 2", "cyan", 300, 200, "down")
essen_körper = Essen("blue", SPIEL_BREITE, SPIEL_HOEHE)

game_over = False
game_started = False

# Maps session_id -> player number (1 or 2)
spieler_sessions = {}


def get_kreise_für_render():
    return spieler1.get_segments() + spieler2.get_segments()


def eat_body(attacker, victim):
    lost_segments = len(victim.body) - 2
    if lost_segments <= 0:
        return

    # zurücksetzen auf zwei Segmente
    victim.body = victim.body[:2]

    # Angreifer wächst um die verlorenen Segmente
    last_segment = attacker.body[-1]
    for _ in range(lost_segments):
        attacker.body.append(körperteil(attacker.farbe, attacker.durchmesser, last_segment.x, last_segment.y))


def game_loop():
    global game_over

    speed = 0.2

    while not game_over:
        länge = len(spieler1.body) + len(spieler2.body)

        if länge >= 20:
            speed = 0.07
        elif länge >= 15:
            speed = 0.10
        elif länge >= 10:
            speed = 0.13
        elif länge >= 5:
            speed = 0.17
        else:
            speed = 0.20

        time.sleep(speed)

        spieler1_ate = essen_körper.berührt(spieler1.get_kopf())
        spieler2_ate = essen_körper.berührt(spieler2.get_kopf())

        spieler1.bewege(SPIEL_BREITE, SPIEL_HOEHE, wachse=spieler1_ate)
        spieler2.bewege(SPIEL_BREITE, SPIEL_HOEHE, wachse=spieler2_ate)

        # Selbst-Kollision
        if spieler1.kollidiert_mit(spieler1.body[1:]) or spieler2.kollidiert_mit(spieler2.body[1:]):
            socketio.emit('zustand', {"status": "game over"})
            game_over = True
            return

        # Kopf-auf-Kopf = Game Over
        if spieler1.get_kopf().x == spieler2.get_kopf().x and spieler1.get_kopf().y == spieler2.get_kopf().y:
            socketio.emit('zustand', {"status": "game over"})
            game_over = True
            return

        # Spieler 1 isst Spieler 2 Körper
        if spieler1.kollidiert_mit(spieler2.body[1:]):
            eat_body(spieler1, spieler2)

        # Spieler 2 isst Spieler 1 Körper
        elif spieler2.kollidiert_mit(spieler1.body[1:]):
            eat_body(spieler2, spieler1)

        if spieler1_ate or spieler2_ate:
            essen_körper.bewege()

        socketio.emit('zustand', {
            "kreise": get_kreise_für_render(),
            "essen": {
                "x": essen_körper.x,
                "y": essen_körper.y,
            },
        })


@app.route("/")
def index():
    return render_template(
        "index.html",
        kreise_für_render=get_kreise_für_render(),
        essen_farbe=essen_körper.get_farbe(),
        essen_x=essen_körper.x,
        essen_y=essen_körper.y,
    )


@socketio.on('connect')
def handle_connect():
    global game_started

    sid = request.sid

    # Assign player number based on connection order
    if len(spieler_sessions) == 0:
        spieler_sessions[sid] = 1
        emit('spieler_nummer', {'nummer': 1})
        print(f"Spieler 1 verbunden: {sid}")
    elif len(spieler_sessions) == 1:
        spieler_sessions[sid] = 2
        emit('spieler_nummer', {'nummer': 2})
        print(f"Spieler 2 verbunden: {sid}")

        # Start game loop only when both players are connected
        if not game_started:
            game_started = True
            t = threading.Thread(target=game_loop, daemon=True)
            t.start()
            # Notify both players that game is starting
            socketio.emit('spiel_start', {})
    else:
        emit('voll', {'nachricht': 'Spiel ist voll!'})
        print(f"Verbindung abgelehnt (voll): {sid}")


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in spieler_sessions:
        nummer = spieler_sessions.pop(sid)
        print(f"Spieler {nummer} getrennt: {sid}")
        socketio.emit('zustand', {"status": "game over"})


@socketio.on('richtung')
def handle_richtung(data):
    sid = request.sid
    nummer = spieler_sessions.get(sid)
    richtung = data.get("richtung")
    if not richtung:
        return

    if nummer == 1:
        spieler1.set_richtung(richtung)
    elif nummer == 2:
        spieler2.set_richtung(richtung)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, port=5001)
