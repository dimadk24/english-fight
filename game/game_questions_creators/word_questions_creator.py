from random import shuffle
from typing import List

from rest_framework.exceptions import APIException

from data.word_pairs import WORD_PAIRS
from game.constants import QUESTIONS_PER_GAME, ANSWERS_PER_QUESTION
from game.game_utils import GameUtils
from game.models import Question, Game


def create_word_questions(game: Game):
    check_language_pairs_number()
    questions = []
    for _ in range(QUESTIONS_PER_GAME):
        questions.append(get_question_to_create(game, questions))
    Question.objects.bulk_create(questions)


def check_language_pairs_number():
    min_number_of_pairs = max(ANSWERS_PER_QUESTION, QUESTIONS_PER_GAME)
    if len(WORD_PAIRS) < min_number_of_pairs:
        raise APIException(
            f"Must have at least {min_number_of_pairs} language pairs to "
            "create a game"
        )


def get_random_language_pair() -> dict:
    index = GameUtils.get_random_int(0, len(WORD_PAIRS) - 1)
    return WORD_PAIRS[index]


def get_question_to_create(
    game: Game, existing_questions: List[Question]
) -> Question:
    while True:
        question_pair = get_random_language_pair()
        existing_question_words = [
            question.question for question in existing_questions
        ]
        new_question_word = question_pair["english_word"]
        if new_question_word not in existing_question_words:
            answer_words = get_question_answers(question_pair)
            return Question(
                game=game,
                question=new_question_word,
                correct_answer=question_pair["russian_word"],
                answer_words=answer_words,
            )


def get_question_answers(question_pair: dict) -> List[str]:
    answers = [question_pair["russian_word"]]
    for _ in range(ANSWERS_PER_QUESTION - 1):
        answers.append(get_wrong_answer(answers))
    shuffle(answers)
    return answers


def get_wrong_answer(existing_answers: List[str]) -> str:
    while True:
        random_language_pair = get_random_language_pair()
        if random_language_pair["russian_word"] not in existing_answers:
            return random_language_pair["russian_word"]
