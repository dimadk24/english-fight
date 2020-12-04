from rest_framework.response import Response

from game.models import AppUser, Question


def authenticate_with_user_1(api_client):
    user = AppUser.objects.create(vk_id=1, username='1', score=2)
    api_client.force_authenticate(user)


def authenticate_with_user_2(api_client):
    user = AppUser.objects.create(vk_id=2, username='2', score=1)
    api_client.force_authenticate(user)


def create_game(api_client) -> Response:
    return api_client.post('/api/game?expand=questions')


def call(api_client, question_id, data: dict):
    return api_client.patch(f'/api/question/{question_id}', data)


def test_sets_correct_selected_question_of_current_user(api_client,
                                                        create_language_pairs):
    authenticate_with_user_1(api_client)
    game = create_game(api_client).data
    question_1 = game['questions'][0]
    question_instance = Question.objects.get(pk=question_1['id'])
    question_word = question_instance.question_word
    language_pair = question_word.english_pair
    correct_answer_word = language_pair.russian_word
    response = call(api_client, question_1['id'],
                    {
                        'selected_answer': correct_answer_word.text,
                    })
    assert response.status_code == 200
    data = response.data
    assert data['is_correct']
    assert data['correct_answer'] == correct_answer_word.text
    assert data['selected_answer'] == correct_answer_word.text


def test_sets_incorrect_selected_question_of_current_user(api_client,
                                                          create_language_pairs):
    authenticate_with_user_1(api_client)
    game = create_game(api_client).data
    question_1 = game['questions'][0]
    question_instance = Question.objects.get(pk=question_1['id'])
    question_word = question_instance.question_word
    language_pair = question_word.english_pair
    correct_answer_word = language_pair.russian_word
    answer_words = question_1['answer_words']
    if not answer_words[0] == correct_answer_word.text:
        incorrect_answer_word = answer_words[0]
    else:
        incorrect_answer_word = answer_words[1]

    response = call(api_client, question_1['id'],
                    {
                        'selected_answer': incorrect_answer_word,
                    })
    assert response.status_code == 200
    data = response.data
    assert not data['is_correct']
    assert data['correct_answer'] == correct_answer_word.text
    assert data['selected_answer'] == incorrect_answer_word


def test_raises_when_try_to_set_selected_question_of_another_user(
    api_client,
    create_language_pairs
):
    authenticate_with_user_1(api_client)
    game = create_game(api_client).data
    question_1 = game['questions'][0]

    authenticate_with_user_2(api_client)
    question_instance = Question.objects.get(pk=question_1['id'])
    question_word = question_instance.question_word
    language_pair = question_word.english_pair
    correct_answer_word = language_pair.russian_word

    response = call(api_client, question_1['id'],
                    {'selected_answer': correct_answer_word.text})
    assert response.status_code == 403
    assert (response.data['detail'] ==
            'У вас недостаточно прав для выполнения данного действия.')

    question_instance = Question.objects.get(pk=question_1['id'])
    assert question_instance.selected_answer is None
