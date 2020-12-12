from datetime import timedelta
from unittest import mock

import pytest
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response

from game.models import AppUser, Game, Question
from language_pairs import get_pair_by_english_word


def post(api_client) -> Response:
    return api_client.post('/api/game')


def get(api_client, game_id) -> Response:
    return api_client.get(f'/api/game/{game_id}')


def assert_not_included_in_questions(word: str):
    assert Question.objects.filter(
        Q(question_word=word) |
        Q(correct_answer=word) |
        Q(answer_words__contains=word)
    ).count() == 0


def do_database_asserts():
    assert Game.objects.count() == 1
    assert Question.objects.count() == 5

    game = Game.objects.get()
    assert game.questions.count() == 5
    assert game.player == AppUser.objects.get(vk_id=1)
    assert game.points == 0
    now = timezone.now()
    assert now - game.created_at < timedelta(minutes=1)

    question_words = [question.question_word for question in
                      game.questions.all()]

    assert len(question_words) == len(set(question_words))

    for question in game.questions.all():
        assert question.correct_answer in question.answer_words
        language_pair = get_pair_by_english_word(question.question_word)
        assert language_pair['russian_word'] == question.correct_answer
        assert question.selected_answer is ''
        assert not question.is_correct

    assert_not_included_in_questions('Ноль')
    assert_not_included_in_questions('Zero')


# run it many times just to ensure it always passes
@pytest.mark.parametrize('i', range(10))
def test_creates_with_real_random(i: int, api_client):
    response = post(api_client)

    assert response.status_code == 201
    offset = i * 5 + 1
    assert response.data['questions'] == [_ + offset for _ in range(5)]
    do_database_asserts()


@mock.patch('game.views.game_view.GameView.get_random_int')
def test_creates_with_fake_random(get_random_int, api_client):
    get_random_int.side_effect = [
        4, 4, 0, 0, 1, 3, 1, 2, 3, 2, 3, 4,
        3, 3, 4, 0, 1, 2, 3,
        0, 1, 2, 3, 4,
        4, 4, 0, 3, 3, 2, 1, 3, 0, 1, 2, 3, 4,
        1, 1, 2, 2, 3, 3, 4, 4, 4, 1, 0, 0,
    ]
    response = post(api_client)
    assert response.status_code == 201
    do_database_asserts()


def test_returns_game_of_current_user(api_client):
    game = post(api_client).data
    response = get(api_client, game['id'])

    assert response.status_code == 200
    data = response.data
    assert data['id']
    assert len(data['questions']) == 5
    assert data['points'] == 0


def test_does_not_return_game_of_another_user(api_client):
    game = post(api_client).data

    user2 = AppUser.objects.create(vk_id=2, username=2)
    api_client.force_authenticate(user2)
    response = get(api_client, game['id'])

    assert response.status_code == 404
    assert response.data['detail'] == 'Страница не найдена.'
