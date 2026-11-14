from spiel_feld import Spiel_Feld


class Data:
    @staticmethod
    def get_game_data(game, game_result=None):
        return {
            "snake": game.snake.get_kreise(),
            "foods": Data.get_food_data(game.normal_essen),
            "small_foods": Data.get_food_data(
                game.small_essen
                if game.current_level.small_f_c
                else None
            ),
            "angry_birds": Data.get_angry_bird_data(game.angry_bird),
            "current_level": game.current_level.number,
            "score": game.score,
            "game_over": game_result is not None or game.game_over,
            "game_result": game_result,
        }

    @staticmethod
    def get_direction_data(game):
        return {"richtung": game.snake.aktuelle_Richtung}

    @staticmethod
    def get_start_game_data(game):
        return {"started": not game.game_over}

    @staticmethod
    def get_finish_game_data(result):
        if result.get("saved") is False:
            return {"saved": False}
        return {
            "score": result["score"],
            "previous_score": result["previous_score"],
            "comparison": result["comparison"],
        }

    @staticmethod
    def get_field_size_data(spielfeld):
        return {
            "field_width": spielfeld.breite,
            "field_height": spielfeld.höhe,
        }

    @staticmethod
    def get_food_data(food=None):
        if food is None:
            return []
        return [Spiel_Feld._shape_to_svg(food)]

    @staticmethod
    def get_angry_bird_data(bird):
        if bird is None:
            return []
        return [
            {
                "cx": bird.x,
                "cy": bird.y,
                "r": bird.durchmesser / 2,
                "color": bird.farbe,
            }
        ]

    @staticmethod
    def get_index_data(game, spielfeld, score_database):
        return {
            "circles": game.snake.get_kreise(),
            "foods": Data.get_food_data(game.normal_essen),
            "small_foods": Data.get_food_data(
                game.small_essen
                if game.current_level.small_f_c
                else None
            ),
            "angry_birds": Data.get_angry_bird_data(game.angry_bird),
            "spielrand": spielfeld.rand,
            "current_level": game.current_level.number,
            "last_result": score_database.get_last_result(),
            "current_score": game.score,
        }
