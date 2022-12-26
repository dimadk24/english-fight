from random import choice, shuffle
from typing import List, Tuple

from django.templatetags.static import static

from data.pictures import PICTURES, PicturesTopic
from game.constants import QUESTIONS_PER_GAME, ANSWERS_PER_QUESTION
from game.models import Game, Question


def create_picture_questions(game: Game) -> List[Question]:
    pictures_topic = choice(PICTURES)  # nosec
    questions = []
    for _ in range(QUESTIONS_PER_GAME):
        questions.append(
            get_question_to_create(game, pictures_topic, questions)
        )
    return questions


def get_question_to_create(
    game: Game,
    pictures_topic: PicturesTopic,
    existing_questions: List[Question],
) -> Question:
    while True:
        new_question_item = get_random_topic_item(pictures_topic)
        new_question_link = static(
            get_file_path(pictures_topic, new_question_item)
        )
        existing_question_links = [
            question.question for question in existing_questions
        ]
        if new_question_link not in existing_question_links:
            answers = get_answers(pictures_topic, new_question_item)
            return Question(
                game=game,
                question=new_question_link,
                answer_words=answers,
                correct_answer=new_question_item[0],
            )


def get_file_path(topic: PicturesTopic, question_item: Tuple[str, str]) -> str:
    topic_number = PICTURES.index(topic) + 1
    dashed_topic = topic.name.replace(" ", "-")
    question_item_number = topic.items.index(question_item) + 1
    extension = question_item[1]
    return (
        f"picture-questions/{topic_number}-{dashed_topic}/"
        f"{question_item_number}.{extension}"
    )


def get_answers(
    topic: PicturesTopic, question_item: Tuple[str, str]
) -> List[str]:
    answers = [question_item[0]]
    for _ in range(ANSWERS_PER_QUESTION - 1):
        answers.append(get_wrong_answer(topic, answers))
    shuffle(answers)
    return answers


def get_wrong_answer(topic: PicturesTopic, existing_answers: List[str]) -> str:
    while True:
        random_item = get_random_topic_item(topic)
        if random_item[0] not in existing_answers:
            return random_item[0]


def get_random_topic_item(pictures_topic: PicturesTopic) -> Tuple[str, str]:
    return choice(pictures_topic.items)  # nosec
