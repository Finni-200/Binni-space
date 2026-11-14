import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "snace"))

from game import Game
from spiel_feld import Spiel_Feld


class FoodTypesTest(unittest.TestCase):
    def test_normal_food_grows_snake_and_small_food_shrinks_snake(self):
        game = Game(Spiel_Feld(400, 300, 0, 20))
        snake = game.snake
        initial_length = len(snake.segments)
        head = snake.segments[0]
        game.normal_essen.x = head.x + snake.durchmesser
        game.normal_essen.y = head.y
        game.tick()

        self.assertEqual(len(snake.segments), initial_length + 1)

        head = snake.segments[0]
        target = (head.x + snake.durchmesser, head.y)
        game.spawn_food(game.normal_essen, exclude={target})
        game.small_essen.x, game.small_essen.y = target
        game.tick()
        self.assertEqual(len(snake.segments), initial_length)
