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

        if self.angry_bird is not None:
            self.angry_bird.move(
                self.snake.min_x,
                self.snake.max_x,
                self.snake.min_y,
                self.snake.max_y,
                self.snake.durchmesser,
            )

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

    def move(self, min_x, max_x, min_y, max_y, distance):
        next_x = self.x + self.direction_x * distance
        next_y = self.y + self.direction_y * distance

        hit_x = next_x < min_x or next_x > max_x
        hit_y = next_y < min_y or next_y > max_y
        if not hit_x and not hit_y:
            self.x = next_x
            self.y = next_y
            return

        if next_x < min_x:
            next_x = min_x
            inward_x = 1
        elif next_x > max_x:
            next_x = max_x
            inward_x = -1
        else:
            inward_x = 0

        if next_y < min_y:
            next_y = min_y
            inward_y = 1
        elif next_y > max_y:
            next_y = max_y
            inward_y = -1
        else:
            inward_y = 0

        reflected_x = -self.direction_x if hit_x else self.direction_x
        reflected_y = -self.direction_y if hit_y else self.direction_y
        max_turn = 90
        if hit_x:
            incidence = math.degrees(
                math.atan2(abs(self.direction_y), abs(self.direction_x))
            )
            max_turn = min(max_turn, 90 - incidence)
        if hit_y:
            incidence = math.degrees(
                math.atan2(abs(self.direction_x), abs(self.direction_y))
            )
            max_turn = min(max_turn, 90 - incidence)

        max_turn = max(0, max_turn - 0.001)
        turn = math.radians(random.uniform(min(2, max_turn), max_turn))
        turn *= random.choice((-1, 1))
        cosine = math.cos(turn)
        sine = math.sin(turn)
        direction_x = reflected_x * cosine - reflected_y * sine
        direction_y = reflected_x * sine + reflected_y * cosine

        if hit_x:
            direction_x = inward_x * abs(direction_x)
        if hit_y:
            direction_y = inward_y * abs(direction_y)
        length = math.hypot(direction_x, direction_y)

        self.x = next_x
        self.y = next_y
        self.direction_x = direction_x / length
        self.direction_y = direction_y / length
