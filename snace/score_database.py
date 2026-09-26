from pathlib import Path
import sqlite3


class ScoreDatabase:
    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path else Path(__file__).with_name("score_history.db")
        self._initialize()

    def _initialize(self):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER NOT NULL,
                    previous_score INTEGER,
                    comparison TEXT NOT NULL
                )
                """
            )

    def save_score(self, score: int) -> dict:
        if isinstance(score, bool) or not isinstance(score, int) or score < 0:
            raise ValueError("Der Score muss eine nicht-negative ganze Zahl sein.")

        with sqlite3.connect(self.db_path) as connection:
            previous_row = connection.execute(
                "SELECT score FROM scores ORDER BY id DESC LIMIT 1"
            ).fetchone()
            previous_score = previous_row[0] if previous_row else None

            if previous_score is None:
                comparison = "erstes Spiel"
            elif score > previous_score:
                comparison = "besser"
            elif score < previous_score:
                comparison = "schlechter"
            else:
                comparison = "gleich"

            connection.execute(
                "INSERT INTO scores (score, previous_score, comparison) VALUES (?, ?, ?)",
                (score, previous_score, comparison),
            )

        return {
            "score": score,
            "previous_score": previous_score,
            "comparison": comparison,
        }

    def get_last_result(self) -> dict | None:
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT score, previous_score, comparison FROM scores ORDER BY id DESC LIMIT 1"
            ).fetchone()

        if row is None:
            return None

        return {
            "score": row[0],
            "previous_score": row[1],
            "comparison": row[2],
        }