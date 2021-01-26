import re
from datetime import timedelta
from unittest import mock

import pytest
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.test import APIClient

from data.pictures import PICTURES, PicturesTopic
from data.word_pairs import get_pair_by_english_word
from enfight import settings
from game.constants import QUESTIONS_PER_GAME
from game.models import AppUser, Game, Question


def post(api_client: APIClient, data=None) -> Response:
    if data is None:
        data = {}
    return api_client.post("/api/game", data)


def get(api_client, game_id) -> Response:
    return api_client.get(f"/api/game/{game_id}")


def assert_not_included_in_questions(word: str):
    assert (
        Question.objects.filter(
            Q(question=word)
            | Q(correct_answer=word)
            | Q(answer_words__contains=word)
        ).count()
        == 0
    )


def do_database_asserts(game_type: str):
    assert Game.objects.count() == 1
    assert Question.objects.count() == 5

    game = Game.objects.get()
    assert game.questions.count() == 5
    assert game.player == AppUser.objects.get(vk_id=1)
    assert game.points == 0
    now = timezone.now()
    assert now - game.created_at < timedelta(minutes=1)

    question_words = [question.question for question in game.questions.all()]

    assert len(question_words) == len(set(question_words))

    for question in game.questions.all():
        assert question.correct_answer in question.answer_words
        if game_type == Game.WORD:
            language_pair = get_pair_by_english_word(question.question)
            assert language_pair["russian_word"] == question.correct_answer
        elif game_type == Game.PICTURE:
            answer_path = question.question
            regex = (
                settings.STATIC_URL
                + r"picture-questions/(\d+)-([a-z\-]+)/(\d+)\..*"
            )
            match = re.match(regex, answer_path)
            assert match
            topic_number = int(match.group(1))
            topic_name = match.group(2).replace('-', ' ')
            picture_number = int(match.group(3))
            found_topic: PicturesTopic = PICTURES[topic_number - 1]
            assert found_topic.name == topic_name
            topic_picture_names = [item[0] for item in found_topic.items]
            assert (
                topic_picture_names[picture_number - 1]
                == question.correct_answer
            )
            assert len(question.answer_words)
            for answer in question.answer_words:
                assert answer in topic_picture_names
        else:
            assert False
        assert question.selected_answer == ""
        assert not question.is_correct

    assert_not_included_in_questions("Ноль")
    assert_not_included_in_questions("Zero")


# run it many times just to ensure it always passes
@pytest.mark.parametrize("i", range(20))
@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_creates_with_real_random(i: int, game_type, api_client):
    response = post(api_client, {"type": game_type})

    assert response.status_code == 201
    question_ids = response.data["questions"]
    assert len(question_ids) == QUESTIONS_PER_GAME
    for question_id in question_ids:
        assert Question.objects.filter(pk=question_id).exists()
    assert response.data["type"] == game_type
    do_database_asserts(game_type)


@mock.patch("game.game_utils.GameUtils.get_random_int")
@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_creates_with_fake_random(get_random_int, game_type, api_client):
    get_random_int.side_effect = [
        4,
        4,
        0,
        0,
        1,
        3,
        1,
        2,
        3,
        2,
        3,
        4,
        3,
        3,
        4,
        0,
        1,
        2,
        3,
        0,
        1,
        2,
        3,
        4,
        4,
        4,
        0,
        3,
        3,
        2,
        1,
        3,
        0,
        1,
        2,
        3,
        4,
        1,
        1,
        2,
        2,
        3,
        3,
        4,
        4,
        4,
        1,
        0,
        0,
    ]
    response = post(api_client, {"type": game_type})
    assert response.status_code == 201
    do_database_asserts(game_type)


def test_returns_game_of_current_user(api_client):
    game = post(api_client).data
    response = get(api_client, game["id"])

    assert response.status_code == 200
    data = response.data
    assert data["id"]
    assert len(data["questions"]) == 5
    assert data["points"] == 0


def test_does_not_return_game_of_another_user(api_client):
    game = post(api_client).data

    user2 = AppUser.objects.create(vk_id=2, username=2)
    api_client.force_authenticate(user2)
    response = get(api_client, game["id"])

    assert response.status_code == 404
    assert response.data["detail"] == "Страница не найдена."
