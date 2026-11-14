import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))
app_module = import_module("app")
Game = import_module("game").Game
ScoreDatabase = import_module("score_database").ScoreDatabase


class AppRoutesTest(unittest.TestCase):
    def setUp(self):
        self.original_game = app_module.game
        self.original_database = app_module.score_database
        self.original_game_result = app_module.game_result
        self.original_started = app_module.game_started.is_set()
        self.original_field_size = (
            app_module.spielfeld.breite,
            app_module.spielfeld.höhe,
        )
        self.database_directory = tempfile.TemporaryDirectory()

        app_module.game = Game(app_module.spielfeld)
        app_module.score_database = ScoreDatabase(
            Path(self.database_directory.name) / "scores.db"
        )
        app_module.game_result = None
        app_module.game_started.clear()
        self.client = app_module.app.test_client()

    def tearDown(self):
        app_module.game = self.original_game
        app_module.score_database = self.original_database
        app_module.game_result = self.original_game_result
        app_module.spielfeld.breite, app_module.spielfeld.höhe = (
            self.original_field_size
        )
        if self.original_started:
            app_module.game_started.set()
        else:
            app_module.game_started.clear()
        self.database_directory.cleanup()

    def test_game_state_route_returns_serialized_game_data(self):
        response = self.client.get("/api/snake")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("snake", data)
        self.assertIn("foods", data)
        self.assertIn("current_level", data)
        self.assertFalse(data["game_over"])

    def test_index_route_renders_game_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<!doctype html>", response.data)

    def test_direction_route_updates_game_and_returns_json(self):
        response = self.client.get("/richtung/up")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"richtung": "up"})
        self.assertEqual(app_module.game.snake.aktuelle_Richtung, "up")

    def test_start_and_finish_routes_return_json(self):
        start_response = self.client.post("/api/start-game")
        finish_response = self.client.post("/api/finish-game")

        self.assertEqual(start_response.get_json(), {"started": True})
        self.assertEqual(
            finish_response.get_json(),
            {
                "score": 0,
                "previous_score": None,
                "comparison": "erstes Spiel",
            },
        )

    def test_invalid_field_size_returns_json_error(self):
        response = self.client.post(
            "/update_field_size",
            json={"width": True, "height": 300},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Ungültige Fenstergröße"})

    def test_field_size_route_resets_game_and_preserves_score(self):
        app_module.game.snake.score = 12

        response = self.client.post(
            "/update_field_size",
            json={"width": 800, "height": 600},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"field_width": 700, "field_height": 500},
        )
        self.assertEqual(app_module.game.score, 12)
