import threading
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from player import Spieler

# Configure Flask to find templates and static files in parent directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))
socketio = SocketIO(app)

# Initialize players and game variables
spieler_sessions = {}
game_started = False
spieler1 = None
spieler2 = None


@socketio.on('connect')
def handle_connect():
    global game_started, spieler1, spieler2

    sid = request.sid

    # Assign player number based on connection order
    if len(spieler_sessions) == 0:
        spieler_sessions[sid] = 1
        spieler1 = Spieler("Spieler 1", (255, 0, 0), 100, 100)
        emit('spieler_nummer', {'nummer': 1})
        print(f"Spieler 1 verbunden: {sid}")
    elif len(spieler_sessions) == 1:
        spieler_sessions[sid] = 2
        spieler2 = Spieler("Spieler 2", (0, 0, 255), 700, 500, "left")
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

    if nummer == 1 and spieler1:
        spieler1.set_richtung(richtung)
    elif nummer == 2 and spieler2:
        spieler2.set_richtung(richtung)


def game_loop():
    """Main game loop for server-side updates"""
    import time
    global game_started, spieler1, spieler2
    while game_started:
        if spieler1 and spieler2:
            spieler1.bewege(800, 600)
            spieler2.bewege(800, 600)
            socketio.emit('zustand', {
                'spieler1': {'body': [(s.x, s.y) for s in spieler1.body]},
                'spieler2': {'body': [(s.x, s.y) for s in spieler2.body]}
            })
        time.sleep(0.05)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)