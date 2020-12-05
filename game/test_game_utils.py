import pytest

from game.game_utils import get_score_for_game


@pytest.mark.parametrize(
    'correct_count,incorrect_count,expected',
    [
        (1, 4, 1),
        (2, 3, 1),
        (3, 2, 4),
        (4, 1, 7),
        (5, 0, 15)
    ])
def test_get_score_for_game(correct_count, incorrect_count, expected):
    assert get_score_for_game(correct_count, incorrect_count) == expected
