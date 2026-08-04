import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from levels import LEVELS, get_level, get_next_level
from snace import Snace


def test_levels_are_available_and_ordered():
    assert len(LEVELS) >= 6
    assert LEVELS[0].number == 1
    assert LEVELS[0].name == "Level 1"
    assert LEVELS[1].number == 2
    assert LEVELS[2].number == 3
    assert LEVELS[5].number == 6


def test_get_level_and_next_level_helpers_work():
    level_2 = get_level(2)
    assert level_2 is not None
    assert level_2.name == "Level 2"
    assert get_next_level(2).number == 3
    assert get_next_level(5).number == 6
    assert get_next_level(6) is None


def test_snake_advances_to_next_level_after_required_food():
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

    snake.normal_essen.x = snake.liste[0].x + snake.durchmesser
    snake.normal_essen.y = snake.liste[0].y
    snake.current_direction = "right"

    first_result = snake.move("right")
    assert first_result["ate_normal_food"] is True
    assert first_result["level_up"] is False

    snake.normal_essen.x = snake.liste[0].x + snake.durchmesser
    snake.normal_essen.y = snake.liste[0].y
    second_result = snake.move("right")

    assert second_result["ate_normal_food"] is True
    assert second_result["level_up"] is True
    assert snake.current_level.number == 2
    assert snake.wartezeit == get_level(2).speed
