import sys
from importlib import import_module
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))
ScoreDatabase = import_module("score_database").ScoreDatabase


def test_score_database_saves_scores_and_compares_each_game(tmp_path):
    database = ScoreDatabase(tmp_path / "scores.db")

    first_result = database.save_score(25)
    second_result = database.save_score(30)
    third_result = database.save_score(20)

    assert first_result == {
        "score": 25,
        "previous_score": None,
        "comparison": "erstes Spiel",
    }
    assert second_result == {
        "score": 30,
        "previous_score": 25,
        "comparison": "besser",
    }
    assert third_result == {
        "score": 20,
        "previous_score": 30,
        "comparison": "schlechter",
    }
    assert database.get_last_result() == third_result


def test_score_database_rejects_invalid_scores(tmp_path):
    database = ScoreDatabase(tmp_path / "scores.db")

    try:
        database.save_score(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Negative Scores must not be accepted")