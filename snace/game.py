import random

from angry_bird import Angry_Bird
from essen import Essen
from levels import get_level_for_length
from snace import Snace


class Game:
    def __init__(self, spielfeld):
        self.spielfeld = spielfeld
        self.snake = Snace.create_snake(spielfeld)
        self.snake.set_direction("right")
        self.normal_essen = Essen(
            "green", self.snake.durchmesser, 0, 0
        )
        self.small_essen = Essen(
            "blue", self.snake.durchmesser / 2, 0, 0
        )
        self.angry_bird = None
        self.current_level = get_level_for_length(self.snake.length)
        self.snake.wartezeit = self.current_level.speed
        self.game_over = False
        self._ensure_level_objects()

    @property
    def score(self):
        return self.snake.score

    @property
    def level(self):
        return self.current_level

    def set_direction(self, direction):
        self.snake.set_direction(direction)

    def update_field_size(self, width, height):
        if not self.spielfeld.update_field_size(width, height):
            return

        score = self.score
        reset_game = type(self)(self.spielfeld)
        self.__dict__.update(reset_game.__dict__)
        self.snake.score = score

    def spawn_food(self, food, exclude=()):
        occupied = {(segment.x, segment.y) for segment in self.snake.segments}
        occupied.update(exclude)
        for other_food in (self.normal_essen, self.small_essen):
            if other_food is not food and (other_food.x, other_food.y) != (0, 0):
                occupied.add((other_food.x, other_food.y))
        if self.angry_bird is not None:
            occupied.add((self.angry_bird.x, self.angry_bird.y))

        candidates = [
            (x, y)
            for x in self._grid_values(self.snake.min_x, self.snake.max_x)
            for y in self._grid_values(self.snake.min_y, self.snake.max_y)
            if (x, y) not in occupied
        ]
        if not candidates:
            raise RuntimeError("Es gibt keine freie Position für weiteres Essen.")
        food.x, food.y = random.choice(candidates)
        return food

    def spawn_angry_bird(self):
        bird = Angry_Bird("#2da44e", self.snake.durchmesser, 0, 0)
        self.spawn_food(bird)
        self.angry_bird = bird
        return bird

    def tick(self):
        if self.game_over:
            return {
                "ate_normal_food": False,
                "level_up": False,
                "game_over": True,
            }

        old_level = self.current_level.number
        old_tail = self.snake.segments[-1]
        moved = self.snake.move(wrap=self.current_level.W == 0)
        if not moved:
            self.game_over = True
            return {
                "ate_normal_food": False,
                "level_up": False,
                "game_over": True,
            }

        head = self.snake.segments[0]
        if any(
            (head.x, head.y) == (segment.x, segment.y)
            for segment in self.snake.segments[1:]
        ):
            self.game_over = True
        if self.angry_bird is not None and (
            head.x,
            head.y,
        ) == (self.angry_bird.x, self.angry_bird.y):
            self.game_over = True

        ate_normal_food = not self.game_over and self._touches(self.normal_essen)
        ate_small_food = not self.game_over and self._touches(self.small_essen)

        if ate_normal_food:
            self.snake.segments.append(
                type(old_tail)(
                    old_tail.farbe,
                    old_tail.durchmesser,
                    old_tail.x,
                    old_tail.y,
                )
            )
            self.snake.length = len(self.snake.segments)
            self.snake.anzahl = self.snake.length
            self.snake.score += 1
            self.normal_essen.x = 0
            self.normal_essen.y = 0
        elif ate_small_food:
            self.snake.segments.pop()
            self.snake.length = len(self.snake.segments)
            self.snake.anzahl = self.snake.length
            self.small_essen.x = 0
            self.small_essen.y = 0
            if self.snake.length <= 1:
                self.game_over = True

        self.current_level = get_level_for_length(self.snake.length)
        self.snake.wartezeit = self.current_level.speed
        self._ensure_level_objects()
        return {
            "ate_normal_food": ate_normal_food,
            "level_up": self.current_level.number > old_level,
            "game_over": self.game_over,
        }

    def _ensure_level_objects(self):
        if self.current_level.normal_f_c and (
            self.normal_essen.x,
            self.normal_essen.y,
        ) == (0, 0):
            self.spawn_food(self.normal_essen)
        elif not self.current_level.normal_f_c:
            self.normal_essen.x = 0
            self.normal_essen.y = 0

        if self.current_level.small_f_c and (
            self.small_essen.x,
            self.small_essen.y,
        ) == (0, 0):
            self.spawn_food(self.small_essen)
        elif not self.current_level.small_f_c:
            self.small_essen.x = 0
            self.small_essen.y = 0

        if self.current_level.Angry_Bird_c and self.angry_bird is None:
            self.spawn_angry_bird()
        elif not self.current_level.Angry_Bird_c:
            self.angry_bird = None

    def _touches(self, item):
        return (self.snake.segments[0].x, self.snake.segments[0].y) == (
            item.x,
            item.y,
        )

    def _grid_values(self, minimum, maximum):
        count = int((maximum - minimum) // self.snake.durchmesser)
        return [
            minimum + index * self.snake.durchmesser
            for index in range(count + 1)
        ]
