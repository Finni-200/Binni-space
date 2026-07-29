import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from snace import Snace


def test_normal_food_grows_snake_and_small_food_shrinks_snake():
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

    initial_length = len(snake.liste)

    snake.normal_essen.x = snake.liste[0].x + snake.durchmesser
    snake.normal_essen.y = snake.liste[0].y
    snake.current_direction = "right"
    snake.move("right")
    assert len(snake.liste) == initial_length + 1

    snake.small_essen.x = snake.liste[0].x + snake.durchmesser
    snake.small_essen.y = snake.liste[0].y
    snake.current_direction = "right"
    snake.move("right")
    assert len(snake.liste) == initial_length
