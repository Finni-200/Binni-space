import math
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from angry_bird import Angry_Bird
from game import Game
from levels import get_level_for_length
from spiel_feld import Spiel_Feld


def test_angry_bird_starts_flying_down_and_to_the_right():
    bird = Angry_Bird("#2da44e", 20, 50, 50)

    bird.move(0, 100, 0, 100, 10)

    assert bird.x == 50 + 10 / math.sqrt(2)
    assert bird.y == 50 + 10 / math.sqrt(2)


def test_wall_bounce_random_angle_is_limited_by_approach_angle():
    bird = Angry_Bird("#2da44e", 20, 95, 50, direction_x=0.8, direction_y=0.6)
    expected_max_turn = 90 - math.degrees(math.atan2(0.6, 0.8))

    with patch("angry_bird.random.uniform", return_value=2) as random_angle:
        with patch("angry_bird.random.choice", return_value=1):
            bird.move(0, 100, 0, 100, 10)

    lower_bound, upper_bound = random_angle.call_args.args
    assert lower_bound == 2
    assert math.isclose(upper_bound, expected_max_turn - 0.001)
    assert bird.x == 100
    assert bird.direction_x < 0
    assert math.isclose(
        math.hypot(bird.direction_x, bird.direction_y),
        1,
    )


def test_game_moves_angry_bird_independently():
    game = Game(Spiel_Feld(600, 400, 0, 20))
    snake = game.snake
    tail = snake.segments[-1]
    for index in range(5):
        snake.segments.append(
            type(tail)(
                tail.farbe,
                tail.durchmesser,
                tail.x - (index + 1) * snake.durchmesser,
                tail.y,
            )
        )
    snake.length = len(snake.segments)
    snake.anzahl = snake.length
    game.current_level = get_level_for_length(snake.length)
    game.angry_bird = Angry_Bird(
        "#2da44e",
        snake.durchmesser,
        snake.min_x,
        snake.min_y,
    )
    start_position = (game.angry_bird.x, game.angry_bird.y)

    game.move_angry_bird()

    assert (game.angry_bird.x, game.angry_bird.y) != start_position
