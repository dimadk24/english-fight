from random import randint

from game.constants import QUESTIONS_PER_GAME


class GameUtils:
    @staticmethod
    def get_score_for_game(correct_questions_count: int) -> int:
        points = correct_questions_count
        incorrect_questions_count = (
            QUESTIONS_PER_GAME - correct_questions_count
        )
        if not incorrect_questions_count:
            points += 5
        return points

    @staticmethod
    def get_random_int(min_num: int, max_num: int):
        return randint(min_num, max_num)  # nosec
