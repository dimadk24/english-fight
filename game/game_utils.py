def get_score_for_game(correct_questions_count,
                       incorrect_questions_count) -> int:
    points = correct_questions_count * 2 - incorrect_questions_count
    if not incorrect_questions_count:
        points += 5
    if points <= 0:
        points = 1
    return points
