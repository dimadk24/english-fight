from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone

from game.models import LanguagePair, Word, AppUser, Game, Question


def authenticate(api_client):
    user = AppUser.objects.create(vk_id=1, username='1', score=2)
    api_client.force_authenticate(user)


def call(api_client):
    authenticate(api_client)
    return api_client.post('/api/game')


def test_raises_when_no_language_pairs(api_client):
    authenticate(api_client)
    with pytest.raises(
        AssertionError,
        match='Must have at least 5 language pairs to create a game'
    ):
        api_client.get('/api/game')


def assert_not_included_in_questions(word: str):
    word = Word.objects.get(text=word)
    assert word.questions_with_question.count() == 0
    assert word.questions_with_answers.count() == 0
    assert word.questions_with_correct_answer.count() == 0


def do_database_asserts():
    assert Game.objects.count() == 1
    assert Question.objects.count() == 5

    game = Game.objects.get()
    assert game.questions.count() == 5
    assert game.player == AppUser.objects.get(vk_id=1)
    assert game.points == 0
    now = timezone.now()
    assert now - game.created_at < timedelta(seconds=1)

    question_words = [question.question_word for question in
                      game.questions.all()]

    assert len(question_words) == len(set(question_words))

    for question in game.questions.all():
        assert question.correct_answer in question.answer_words.all()
        language_pair = LanguagePair.objects.get(
            english_word=question.question_word)
        assert language_pair.russian_word == question.correct_answer
        assert question.selected_answer is None
        assert not question.is_correct

    assert_not_included_in_questions('Ноль')
    assert_not_included_in_questions('Zero')


# run it many times just to ensure it always passes
@pytest.mark.parametrize('i', range(10))
def test_creates_with_real_random(i: int, api_client, create_language_pairs):
    response = call(api_client)

    assert response.status_code == 201
    offset = i * 5 + 1
    assert response.data['questions'] == [_ + offset for _ in range(5)]
    do_database_asserts()


@mock.patch('game.views.game_view.GameView.get_random_int')
def test_creates_with_fake_random(get_random_int, api_client,
                                  create_language_pairs):
    get_random_int.side_effect = [
        4, 4, 0, 0, 1, 3, 1, 2, 3, 2, 3, 4,
        3, 3, 4, 0, 1, 2, 3,
        0, 1, 2, 3, 4,
        4, 4, 0, 3, 3, 2, 1, 3, 0, 1, 2, 3, 4,
        1, 1, 2, 2, 3, 3, 4, 4, 4, 1, 0, 0,
    ]
    response = call(api_client)
    assert response.status_code == 201
    do_database_asserts()
