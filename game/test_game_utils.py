import pytest

from game.game_utils import GameUtils


@pytest.mark.parametrize(
    "correct_count,expected",
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 15),
    ],
)
def test_get_score_for_game(correct_count, expected):
    assert GameUtils.get_score_for_game(correct_count) == expected
