import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from snace import Snace


def test_eating_food_grows_snake_and_spawns_new_food():
    snake = Snace(
        x_1=100,
        y=100,
        farbe="red",
        farbe_1="green",
        durchmesser=20,
        anzahl=4,
        wartezeit=100,
        spielfeld_width=200,
        spielfeld_height=200,
        spielrand=0,
        farbe_essen="blue",
        durchmesser_essen=10,
    )

    old_food_x = snake.essen.x
    old_food_y = snake.essen.y

    snake.essen.x = snake.liste[0].x + snake.durchmesser
    snake.essen.y = snake.liste[0].y
    snake.aktuelle_Richtung = "right"

    snake.move("right")

    assert len(snake.liste) == 5
    assert (snake.essen.x, snake.essen.y) != (old_food_x, old_food_y)
    assert all((segment.x, segment.y) != (snake.essen.x, snake.essen.y) for segment in snake.liste)
