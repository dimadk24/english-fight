import pytest

from data.word_pairs import get_pair_by_english_word
from game.constants import QUESTIONS_PER_GAME
from game.models import AppUser, Question, Game, GameDefinition
from game.test_question_utils import (
    create_single_player_game,
    set_correct_answer_to_question,
    set_incorrect_answer_to_question,
    update_question,
    get_correct_answer_data_for_picture_question,
)


def authenticate_with_user_2(api_client):
    user = AppUser.objects.create(vk_id=2, username="2")
    api_client.force_authenticate(user)


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_sets_correct_selected_question_of_current_user(api_client, game_type):
    game = create_single_player_game(api_client, game_type)
    question_1 = game["questions"][0]
    (response, correct_answer_word) = set_correct_answer_to_question(
        api_client, question_1, game_type
    )

    assert response.status_code == 200
    data = response.data
    assert data["is_correct"]
    assert data["correct_answer"] == correct_answer_word
    assert data["selected_answer"] == correct_answer_word

    game = Game.objects.get()
    assert game.points == 0


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_sets_incorrect_selected_question_of_current_user(
    api_client, game_type
):
    game = create_single_player_game(api_client, game_type)
    question_1 = game["questions"][0]
    (
        response,
        correct_answer_word,
        incorrect_answer_word,
    ) = set_incorrect_answer_to_question(api_client, question_1, game_type)

    assert response.status_code == 200
    data = response.data
    assert not data["is_correct"]
    assert data["correct_answer"] == correct_answer_word
    assert data["selected_answer"] == incorrect_answer_word

    game = Game.objects.get()
    assert game.points == 0


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_raises_when_try_to_set_selected_question_of_another_user(
    api_client, game_type
):
    game = create_single_player_game(api_client, game_type)
    question_1 = game["questions"][0]

    authenticate_with_user_2(api_client)
    question_instance = Question.objects.get(pk=question_1["id"])
    question_word = question_instance.question
    if game_type == GameDefinition.WORD:
        language_pair = get_pair_by_english_word(question_word)
        correct_answer_word = language_pair["russian_word"]
    else:
        _, item = get_correct_answer_data_for_picture_question(
            question_instance
        )
        correct_answer_word = item[0]

    response = update_question(
        api_client, question_1["id"], {"selected_answer": correct_answer_word}
    )
    assert response.status_code == 404
    assert response.data["detail"] == "Страница не найдена."

    question_instance = Question.objects.get(pk=question_1["id"])
    assert question_instance.selected_answer == ""

    game = Game.objects.get()
    assert game.points == 0


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_updates_points_of_game_when_no_correct_questions(
    api_client, game_type
):
    game = create_single_player_game(api_client, game_type)
    questions = game["questions"]
    assert len(questions) == QUESTIONS_PER_GAME

    game = Game.objects.get()
    assert game.points == 0
    assert game.player.score == 0

    for question in questions:
        set_incorrect_answer_to_question(api_client, question, game_type)

    game = Game.objects.get()
    assert game.points == 0
    assert game.player.score == 0


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_updates_points_of_game_when_has_correct_questions(
    api_client, game_type
):
    game = create_single_player_game(api_client, game_type)
    questions = game["questions"]

    game = Game.objects.get()
    assert game.points == 0
    assert game.player.score == 0

    set_correct_answer_to_question(api_client, questions[0], game_type)
    set_incorrect_answer_to_question(api_client, questions[1], game_type)
    set_incorrect_answer_to_question(api_client, questions[2], game_type)
    set_correct_answer_to_question(api_client, questions[3], game_type)
    set_correct_answer_to_question(api_client, questions[4], game_type)
    set_correct_answer_to_question(api_client, questions[5], game_type)
    set_incorrect_answer_to_question(api_client, questions[6], game_type)
    set_correct_answer_to_question(api_client, questions[7], game_type)
    set_incorrect_answer_to_question(api_client, questions[8], game_type)
    set_correct_answer_to_question(api_client, questions[9], game_type)

    game = Game.objects.get()
    assert game.points == 6
    assert game.player.score == 6


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_updates_points_of_game_when_all_correct_questions(
    api_client, game_type
):
    game = create_single_player_game(api_client, game_type)
    questions = game["questions"]
    assert len(questions) == QUESTIONS_PER_GAME

    game = Game.objects.get()
    assert game.points == 0
    assert game.player.score == 0

    for question in questions:
        set_correct_answer_to_question(api_client, question, game_type)

    game = Game.objects.get()
    assert game.points == 15
    assert game.player.score == 15


@pytest.mark.parametrize("game_type", ["word", "picture"])
def test_set_correct_score_to_user_after_2_games(api_client, game_type):
    game1 = create_single_player_game(api_client, game_type)
    questions = game1["questions"]

    game1 = Game.objects.get()
    assert game1.player.score == 0

    for question in questions[0:-1]:
        set_incorrect_answer_to_question(api_client, question, game_type)
    set_correct_answer_to_question(api_client, questions[-1], game_type)

    game1 = Game.objects.get()
    assert game1.player.score == 1

    game2 = create_single_player_game(api_client, game_type)
    questions = game2["questions"]

    game2 = Game.objects.get(pk=game2["id"])

    assert game2.player == game1.player
    assert game2.player.score == 1

    for question in questions:
        set_correct_answer_to_question(api_client, question, game_type)

    game2 = Game.objects.get(pk=game2.id)
    assert game2.player.score == 16
