import re
from typing import Tuple

from django.conf import settings
from rest_framework.response import Response

from data.pictures import PicturesTopic, PICTURES
from data.word_pairs import get_pair_by_english_word
from game.models import GameDefinition, Question


def create_single_player_game(api_client, game_type: str) -> Response:
    game_def = api_client.post(
        "/api/game_definition", {"type": game_type}
    ).data
    return api_client.post(
        "/api/game?expand=questions", {"game_definition": game_def["id"]}
    ).data


def get_correct_answer_data_for_picture_question_path(
    answer_path: str,
) -> Tuple[PicturesTopic, Tuple[str, str]]:
    regex = (
        settings.STATIC_URL + r"picture-questions/(\d+)-([a-z\-]+)/(\d+)\..*"
    )
    match = re.match(regex, answer_path)
    assert match
    topic_number = int(match.group(1))
    topic_name = match.group(2).replace("-", " ")
    picture_number = int(match.group(3))
    found_topic: PicturesTopic = PICTURES[topic_number - 1]
    assert found_topic.name == topic_name
    found_item = found_topic.items[picture_number - 1]
    return found_topic, found_item


def get_correct_answer_data_for_picture_question(
    question: Question,
) -> Tuple[PicturesTopic, Tuple[str, str]]:
    answer_path = question.question
    return get_correct_answer_data_for_picture_question_path(answer_path)


def update_question(api_client, question_id, data: dict):
    return api_client.patch(f"/api/question/{question_id}", data)


def get_correct_answer_to_question(question_word: str, game_type: str) -> str:
    if game_type == GameDefinition.WORD:
        language_pair = get_pair_by_english_word(question_word)
        return language_pair["russian_word"]
    _, item = get_correct_answer_data_for_picture_question_path(question_word)
    return item[0]


def set_correct_answer_to_question(api_client, question: dict, game_type: str):
    question_instance = Question.objects.get(pk=question["id"])
    question_word = question_instance.question
    answer = get_correct_answer_to_question(question_word, game_type)
    response = update_question(
        api_client,
        question["id"],
        {
            "selected_answer": answer,
        },
    )
    return response, answer


def set_incorrect_answer_to_question(
    api_client, question: dict, game_type: str
):
    question_instance = Question.objects.get(pk=question["id"])
    question_word = question_instance.question
    correct_answer_word = get_correct_answer_to_question(
        question_word, game_type
    )
    answer_words = question["answer_words"]
    if not answer_words[0] == correct_answer_word:
        incorrect_answer_word = answer_words[0]
    else:
        incorrect_answer_word = answer_words[1]

    response = update_question(
        api_client,
        question["id"],
        {
            "selected_answer": incorrect_answer_word,
        },
    )
    return response, correct_answer_word, incorrect_answer_word
