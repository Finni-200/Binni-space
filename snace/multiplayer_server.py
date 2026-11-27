from threading import Lock
from uuid import uuid4
from flask import Flask, jsonify, request


app = Flask(__name__)
MIN_PLAYERS = 2
MAX_PLAYERS = 3
MAX_NAME_LENGTH = 20

players = {}
game_started = False
lobby_lock = Lock()


@app.get("/")
def server_status():
    return "Multiplayer-Server ist gestartet."


@app.get("/api/status")
def lobby_status():
    with lobby_lock:
        return jsonify(
            {
                "players": list(players.values()),
                "player_count": len(players),
                "minimum_players": MIN_PLAYERS,
                "maximum_players": MAX_PLAYERS,
                "can_start": (
                    MIN_PLAYERS <= len(players) <= MAX_PLAYERS and not game_started
                ),
                "started": game_started,
            }
        )


@app.post("/api/join")
def join_lobby():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Ein JSON-Objekt mit einem Namen wird benötigt."}), 400
    

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Bitte gib einen Namen ein."}), 400
    name = name.strip()
    if len(name) > MAX_NAME_LENGTH:
        return jsonify(
            {"error": f"Der Name darf höchstens {MAX_NAME_LENGTH} Zeichen lang sein."}
        ), 400

    with lobby_lock:
        if game_started:
            return jsonify({"error": "Das Spiel wurde bereits gestartet."}), 409
        if len(players) >= MAX_PLAYERS:
            return jsonify({"error": "Die Lobby ist voll."}), 409

        player = {"id": uuid4().hex, "name": name}
        players[player["id"]] = player
        return jsonify(
            {
                "player": player,
                "player_count": len(players),
                "can_start": len(players) >= MIN_PLAYERS and not game_started,
            }
        ), 201


@app.post("/api/leave")
def leave_lobby():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("player_id"), str):
        return jsonify({"error": "Eine Spieler-ID wird benötigt."}), 400

    global game_started
    with lobby_lock:
        if players.pop(data["player_id"], None) is None:
            return jsonify({"error": "Spieler nicht in der Lobby gefunden."}), 404
        if len(players) < MIN_PLAYERS:
            game_started = False
        return jsonify({"left": True, "player_count": len(players)})


@app.post("/api/start")
def start_game():
    global game_started
    with lobby_lock:
        if len(players) < MIN_PLAYERS:
            return jsonify(
                {"error": f"Mindestens {MIN_PLAYERS} Spieler werden benötigt."}
            ), 409
        if game_started:
            return jsonify({"error": "Das Spiel wurde bereits gestartet."}), 409
        game_started = True
        return jsonify({"started": True, "players": list(players.values())})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
