import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from game import Game
from spiel_feld import Spiel_Feld


class FoodLogicTest(unittest.TestCase):
    def test_eating_food_grows_snake_and_spawns_new_food(self):
        game = Game(Spiel_Feld(200, 200, 0, 20))
        snake = game.snake
        initial_length = len(snake.segments)
        head = snake.segments[0]
        consumed_position = (head.x + snake.durchmesser, head.y)

        game.normal_essen.x, game.normal_essen.y = consumed_position
        game.tick()

        self.assertEqual(len(snake.segments), initial_length + 1)
        self.assertEqual(game.score, 1)
        self.assertNotEqual(
            (game.normal_essen.x, game.normal_essen.y),
            consumed_position,
        )
        self.assertTrue(
            all(
                (segment.x, segment.y)
                != (game.normal_essen.x, game.normal_essen.y)
                for segment in snake.segments
            )
        )
