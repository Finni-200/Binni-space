import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from levels import LEVELS, WINNER, get_level, get_level_for_length, get_next_level
from snace import Snace


def test_levels_are_available_and_ordered():
    assert len(LEVELS) == 10
    assert LEVELS[0].number == 1
    assert LEVELS[0].name == "Level 1"
    assert LEVELS[1].number == 2
    assert LEVELS[2].number == 3
    assert LEVELS[5].number == 6
    assert LEVELS[-1].number == WINNER
    assert all(level.description for level in LEVELS)


def test_get_level_and_next_level_helpers_work():
    level_2 = get_level(2)
    assert level_2 is not None
    assert level_2.name == "Level 2"
    assert get_next_level(2).number == 3
    assert get_next_level(5).number == 6
    assert get_next_level(6).number == 7
    assert get_next_level(9).number == WINNER
    assert get_next_level(WINNER) is None


def test_get_level_for_length_uses_the_level_thresholds():
    assert get_level_for_length(4).number == 1
    assert get_level_for_length(5).number == 2
    assert get_level_for_length(19).number == 9
    assert get_level_for_length(20).number == WINNER


def test_green_mouth_obstacle_starts_at_angry_bird_level():
    snake = Snace(
        x_1=200,
        y=200,
        farbe="red",
        farbe_1="green",
        durchmesser=20,
        anzahl=9,
        wartezeit=100,
        spielfeld_width=400,
        spielfeld_height=400,
        spielrand=0,
        farbe_essen="blue",
        durchmesser_essen=10,
    )

    angry_birds = snake.get_angry_bird_data()

    assert len(angry_birds) == 1
    assert angry_birds[0]["color"] == "#2da44e"
    assert angry_birds[0]["r"] == 10


def test_green_mouth_obstacle_follows_snake_one_step_at_a_time():
    snake = Snace(
        x_1=200,
        y=200,
        farbe="red",
        farbe_1="green",
        durchmesser=20,
        anzahl=9,
        wartezeit=100,
        spielfeld_width=400,
        spielfeld_height=400,
        spielrand=0,
        farbe_essen="blue",
        durchmesser_essen=10,
    )
    snake.normal_essen.x = 20
    snake.normal_essen.y = 20
    snake.aktuelle_Richtung = "right"
    snake.angry_bird = {"cx": 20, "cy": 200, "r": 10, "color": "#2da44e"}

    snake.move("right")

    assert snake.angry_bird["cx"] == 40
    assert snake.angry_bird["cy"] == 200


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
    snake.aktuelle_Richtung = "right"

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
    assert snake.score == 2
