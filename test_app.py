import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "snace"))

from app import app


def test_homepage():
    with app.test_client() as client:
        response = client.get("/")
        print("HOME STATUS:", response.status_code)
        print("HOME LENGTH:", len(response.data))
        if response.status_code == 200:
            print("Homepage erfolgreich geladen.")
        else:
            print("Fehler beim Laden der Homepage.")


def test_move():
    with app.test_client() as client:
        response = client.get(
            "/move",
            query_string={
                "richtung1": "right",
                "richtung2": "down",
                "breite": 1200,
                "hoehe": 800,
            },
        )
        print("MOVE STATUS:", response.status_code)
        print("MOVE JSON:", response.get_json())


if __name__ == "__main__":
    test_homepage()
    print("---")
    test_move()
