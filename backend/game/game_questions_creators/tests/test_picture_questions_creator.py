from pathlib import Path

from django.conf import settings

from data.pictures import PICTURES
from game.constants import QUESTIONS_PER_GAME, ANSWERS_PER_QUESTION
from game.game_questions_creators.picture_questions_creator import (
    get_file_path,
)


def test_get_file_path():
    assert len(PICTURES)
    for picture_topic in PICTURES:
        assert len(picture_topic.items)
        for item in picture_topic.items:
            file_path = get_file_path(picture_topic, item).replace(
                "picture-questions", "static_pictures"
            )
            full_path: Path = settings.BASE_DIR / "data" / file_path
            assert full_path.exists()


def test_ensure_each_topic_has_enough_items():
    assert len(PICTURES)
    for picture_topic in PICTURES:
        items_number = len(picture_topic.items)
        assert items_number >= QUESTIONS_PER_GAME
        assert items_number >= ANSWERS_PER_QUESTION
