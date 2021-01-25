from random import randint, shuffle
from typing import List

from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from data.word_pairs import WORD_PAIRS
from game.constants import QUESTIONS_PER_GAME, ANSWERS_PER_QUESTION
from game.models import Question, Game
from game.serializers.game_serializer import GameSerializer


class GameView(CreateAPIView, RetrieveAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(player=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer: GameSerializer):
        serializer.save()
        min_number_of_pairs = max(ANSWERS_PER_QUESTION, QUESTIONS_PER_GAME)
        if len(WORD_PAIRS) < min_number_of_pairs:
            raise APIException(
                f"Must have at least {min_number_of_pairs} language pairs to "
                "create a game"
            )
        self.create_questions(serializer.instance)

    @staticmethod
    def get_random_int(min_num: int, max_num: int):
        return randint(min_num, max_num)  # nosec

    def get_random_language_pair(self) -> dict:
        index = GameView.get_random_int(0, len(WORD_PAIRS) - 1)
        return WORD_PAIRS[index]

    def create_questions(self, game: Game):
        questions = []
        for _ in range(QUESTIONS_PER_GAME):
            questions.append(self.get_question_to_create(game, questions))
        Question.objects.bulk_create(questions)

    def get_question_to_create(
        self, game: Game, existing_questions: List[Question]
    ) -> Question:
        while True:
            question_pair = self.get_random_language_pair()
            existing_question_words = [
                question.question for question in existing_questions
            ]
            new_question_word = question_pair["english_word"]
            if new_question_word not in existing_question_words:
                answer_words = self.get_question_answers(question_pair)
                return Question(
                    game=game,
                    question=new_question_word,
                    correct_answer=question_pair["russian_word"],
                    answer_words=answer_words,
                )

    def get_question_answers(self, question_pair: dict) -> List[str]:
        answers = [question_pair["russian_word"]]
        for _ in range(ANSWERS_PER_QUESTION - 1):
            answers.append(self.get_wrong_answer(answers))
        shuffle(answers)
        return answers

    def get_wrong_answer(self, existing_answers: List[str]) -> str:
        while True:
            random_language_pair = self.get_random_language_pair()
            if random_language_pair["russian_word"] not in existing_answers:
                return random_language_pair["russian_word"]
