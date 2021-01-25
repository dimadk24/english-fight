from random import randint


class GameUtils:
    @staticmethod
    def get_score_for_game(
        correct_questions_count, incorrect_questions_count
    ) -> int:
        points = correct_questions_count * 2 - incorrect_questions_count
        if not incorrect_questions_count:
            points += 5
        if points <= 0:
            points = 1
        return points

    @staticmethod
    def get_random_int(min_num: int, max_num: int):
        return randint(min_num, max_num)  # nosec
