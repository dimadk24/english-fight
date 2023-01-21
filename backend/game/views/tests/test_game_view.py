from datetime import timedelta
from unittest import mock

import pytest
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.test import APIClient

from data.word_pairs import get_pair_by_english_word
from game.constants import QUESTIONS_PER_GAME
from game.models import AppUser, Game, Question, GameDefinition
from game.test_question_utils import (
    get_correct_answer_data_for_picture_question,
)
from test_utils import print_random_state


def post_game_definition(api_client: APIClient, data=None) -> Response:
    if data is None:
        data = {}
    return api_client.post("/api/game_definition", data)


def post_game(api_client: APIClient, data=None) -> Response:
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
    current_user = AppUser.objects.get(vk_id=1)

    assert GameDefinition.objects.count() == 1
    game_definition: GameDefinition = GameDefinition.objects.get()
    assert game_definition.creator == current_user
    assert list(game_definition.players.all()) == []
    assert game_definition.type == game_type
    now = timezone.now()
    assert now - game_definition.created_at < timedelta(minutes=1)

    assert Game.objects.count() == 1
    assert Question.objects.count() == QUESTIONS_PER_GAME

    game = Game.objects.get()
    assert game.game_definition == game_definition
    assert game.questions.count() == QUESTIONS_PER_GAME
    assert game.player == current_user
    assert game.points == 0
    now = timezone.now()
    assert now - game.created_at < timedelta(minutes=1)

    question_words = [question.question for question in game.questions.all()]

    assert len(question_words) == len(set(question_words))

    for question in game.questions.all():
        assert question.correct_answer in question.answer_words
        if game_type == GameDefinition.WORD:
            language_pair = get_pair_by_english_word(question.question)
            assert language_pair["russian_word"] == question.correct_answer
        elif game_type == GameDefinition.PICTURE:
            topic, item = get_correct_answer_data_for_picture_question(
                question
            )
            assert item[0] == question.correct_answer
            assert len(question.answer_words)
            topic_picture_names = [item[0] for item in topic.items]
            for answer in question.answer_words:
                assert answer in topic_picture_names
        else:
            assert False
        assert question.selected_answer == ""
        assert not question.is_correct

    assert_not_included_in_questions("Ноль")
    assert_not_included_in_questions("Zero")


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_creates_with_real_random(game_type, api_client):
    print_random_state()
    game_definition_response = post_game_definition(
        api_client, {"type": game_type}
    )
    assert game_definition_response.status_code == 201

    game_response = post_game(
        api_client, {"game_definition": game_definition_response.data["id"]}
    )

    assert game_response.status_code == 201
    question_ids = game_response.data["questions"]
    assert len(question_ids) == QUESTIONS_PER_GAME
    for question_id in question_ids:
        assert Question.objects.filter(pk=question_id).exists()
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
        1,
        10,
        2,
        3,
        4,
        5,
        7,
        1,
        3,
        0,
        1,
        4,
        7,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        11,
        3,
        36,
        2,
        59,
        98,
    ]
    game_definition_response = post_game_definition(
        api_client, {"type": game_type}
    )
    assert game_definition_response.status_code == 201
    game_def = game_definition_response.data
    assert game_def["type"] == game_type
    assert isinstance(game_def["id"], str)
    assert isinstance(game_def["creator"], int)
    assert isinstance(game_def["players"], list)

    game_response = post_game(api_client, {"game_definition": game_def["id"]})

    question_ids = game_response.data["questions"]
    assert len(question_ids) == QUESTIONS_PER_GAME
    for question_id in question_ids:
        assert Question.objects.filter(pk=question_id).exists()

    assert game_response.status_code == 201
    do_database_asserts(game_type)


def test_returns_game_of_current_user(api_client):
    game_def = post_game_definition(api_client, {"type": "word"})
    game = post_game(api_client, {"game_definition": game_def.data["id"]}).data
    response = get(api_client, game["id"])

    assert response.status_code == 200
    data = response.data
    assert data["id"]
    assert len(data["questions"]) == QUESTIONS_PER_GAME
    assert data["points"] == 0


def test_does_not_return_game_of_another_user(api_client):
    game_def_response = post_game_definition(api_client, {"type": "word"})
    game = post_game(
        api_client, {"game_definition": game_def_response.data["id"]}
    ).data

    user2 = AppUser.objects.create(vk_id=2, username=2)
    api_client.force_authenticate(user2)
    response = get(api_client, game["id"])

    assert response.status_code == 404
    assert response.data["detail"] == "Страница не найдена."


def test_does_not_allow_to_set_creator(api_client):
    first_user = AppUser.objects.create(vk_id=2, username=2)
    api_client.force_authenticate(first_user)
    second_user = AppUser.objects.create(vk_id=3, username=3)

    game_def_response = post_game_definition(
        api_client, {"type": "word", "creator": second_user.id}
    )
    assert game_def_response.status_code == 201

    game_def = GameDefinition.objects.get(id=game_def_response.data["id"])
    assert game_def.creator_id == first_user.id
    assert game_def_response.data["creator"] == first_user.id


def test_does_not_allow_to_set_players(api_client):
    first_user = AppUser.objects.create(vk_id=2, username=2)
    api_client.force_authenticate(first_user)
    second_user = AppUser.objects.create(vk_id=3, username=3)

    game_def_response = post_game_definition(
        api_client, {"type": "word", "players": [second_user.id]}
    )
    assert game_def_response.status_code == 201

    game_def = GameDefinition.objects.get(id=game_def_response.data["id"])
    assert list(game_def.players.all()) == []
    assert game_def_response.data["players"] == []
