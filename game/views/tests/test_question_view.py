from rest_framework.response import Response

from data.word_pairs import get_pair_by_english_word
from game.models import AppUser, Question, Game


def authenticate_with_user_2(api_client):
    user = AppUser.objects.create(vk_id=2, username="2")
    api_client.force_authenticate(user)


def create_game(api_client) -> Response:
    return api_client.post("/api/game?expand=questions").data


def call(api_client, question_id, data: dict):
    return api_client.patch(f"/api/question/{question_id}", data)


def set_correct_answer_to_question(api_client, question: dict):
    question_instance = Question.objects.get(pk=question["id"])
    question_word = question_instance.question
    language_pair = get_pair_by_english_word(question_word)
    correct_answer_word = language_pair["russian_word"]
    response = call(
        api_client,
        question["id"],
        {
            "selected_answer": correct_answer_word,
        },
    )
    return response, correct_answer_word


def set_incorrect_answer_to_question(api_client, question: dict):
    question_instance = Question.objects.get(pk=question["id"])
    question_word = question_instance.question
    language_pair = get_pair_by_english_word(question_word)
    correct_answer_word = language_pair["russian_word"]
    answer_words = question["answer_words"]
    if not answer_words[0] == correct_answer_word:
        incorrect_answer_word = answer_words[0]
    else:
        incorrect_answer_word = answer_words[1]

    response = call(
        api_client,
        question["id"],
        {
            "selected_answer": incorrect_answer_word,
        },
    )
    return response, correct_answer_word, incorrect_answer_word


def test_sets_correct_selected_question_of_current_user(api_client):
    game = create_game(api_client)
    question_1 = game["questions"][0]
    (response, correct_answer_word) = set_correct_answer_to_question(
        api_client, question_1
    )

    assert response.status_code == 200
    data = response.data
    assert data["is_correct"]
    assert data["correct_answer"] == correct_answer_word
    assert data["selected_answer"] == correct_answer_word

    game = Game.objects.get()
    assert game.points == 0


def test_sets_incorrect_selected_question_of_current_user(api_client):
    game = create_game(api_client)
    question_1 = game["questions"][0]
    (
        response,
        correct_answer_word,
        incorrect_answer_word,
    ) = set_incorrect_answer_to_question(api_client, question_1)

    assert response.status_code == 200
    data = response.data
    assert not data["is_correct"]
    assert data["correct_answer"] == correct_answer_word
    assert data["selected_answer"] == incorrect_answer_word

    game = Game.objects.get()
    assert game.points == 0


def test_raises_when_try_to_set_selected_question_of_another_user(api_client):
    game = create_game(api_client)
    question_1 = game["questions"][0]

    authenticate_with_user_2(api_client)
    question_instance = Question.objects.get(pk=question_1["id"])
    question_word = question_instance.question
    language_pair = get_pair_by_english_word(question_word)
    correct_answer_word = language_pair["russian_word"]

    response = call(
        api_client, question_1["id"], {"selected_answer": correct_answer_word}
    )
    assert response.status_code == 404
    assert response.data["detail"] == "Страница не найдена."

    question_instance = Question.objects.get(pk=question_1["id"])
    assert question_instance.selected_answer == ""

    game = Game.objects.get()
    assert game.points == 0


def test_updates_points_of_game_when_no_correct_questions(api_client):
    game = create_game(api_client)
    questions = game["questions"]
    assert len(questions) == 5

    game = Game.objects.get()
    assert game.points == 0
    assert game.player.score == 0

    for question in questions:
        set_incorrect_answer_to_question(api_client, question)

    game = Game.objects.get()
    assert game.points == 1
    assert game.player.score == 1


def test_updates_points_of_game_when_has_correct_questions(api_client):
    game = create_game(api_client)
    questions = game["questions"]

    game = Game.objects.get()
    assert game.points == 0
    assert game.player.score == 0

    set_correct_answer_to_question(api_client, questions[0])
    set_incorrect_answer_to_question(api_client, questions[1])
    set_incorrect_answer_to_question(api_client, questions[2])
    set_correct_answer_to_question(api_client, questions[3])
    set_correct_answer_to_question(api_client, questions[4])

    game = Game.objects.get()
    assert game.points == 4
    assert game.player.score == 4


def test_updates_points_of_game_when_all_correct_questions(api_client):
    game = create_game(api_client)
    questions = game["questions"]
    assert len(questions) == 5

    game = Game.objects.get()
    assert game.points == 0
    assert game.player.score == 0

    for question in questions:
        set_correct_answer_to_question(api_client, question)

    game = Game.objects.get()
    assert game.points == 15
    assert game.player.score == 15


def test_set_correct_score_to_user_after_2_games(api_client):
    game1 = create_game(api_client)
    questions = game1["questions"]

    game1 = Game.objects.get()
    assert game1.player.score == 0

    for question in questions:
        set_incorrect_answer_to_question(api_client, question)

    game1 = Game.objects.get()
    assert game1.player.score == 1

    game2 = create_game(api_client)
    questions = game2["questions"]

    game2 = Game.objects.get(pk=game2["id"])

    assert game2.player == game1.player
    assert game2.player.score == 1

    for question in questions:
        set_correct_answer_to_question(api_client, question)

    game2 = Game.objects.get(pk=game2.id)
    assert game2.player.score == 16
