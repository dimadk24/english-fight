from random import randint, shuffle
from typing import List

from rest_framework.generics import CreateAPIView

from game.constants import QUESTIONS_PER_GAME, ANSWERS_PER_QUESTION
from game.models import LanguagePair, Word, Question, Game
from game.serializers.game_serializer import GameSerializer


class GameView(CreateAPIView):
    serializer_class = GameSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filtered_pairs = LanguagePair.objects.filter(
            visible=True).values('id')
        min_number_of_pairs = max(ANSWERS_PER_QUESTION, QUESTIONS_PER_GAME)
        assert len(self.filtered_pairs) >= min_number_of_pairs, (
            f'Must have at least {min_number_of_pairs} language pairs to '
            'create a game')

    def perform_create(self, serializer: GameSerializer):
        serializer.save()
        self.create_questions(serializer.instance)

    @staticmethod
    def get_random_int(min_num: int, max_num: int):
        return randint(min_num, max_num)

    def get_random_language_pair(self) -> LanguagePair:
        index = GameView.get_random_int(0, len(self.filtered_pairs) - 1)
        pk = self.filtered_pairs[index]['id']
        return LanguagePair.objects.get(pk=pk)

    def create_questions(self, game: Game):
        for _ in range(QUESTIONS_PER_GAME):
            self.create_question(game)

    def create_question(self, game: Game):
        while True:
            question_pair: LanguagePair = self.get_random_language_pair()
            existing_question_words = [question.question_word for
                                       question in game.questions.all()]
            new_question_word = question_pair.english_word
            if new_question_word not in existing_question_words:
                answer_words = self.get_question_answers(question_pair)
                question = Question.objects.create(
                    game=game,
                    question_word=new_question_word,
                    correct_answer=question_pair.russian_word,
                )
                question.answer_words.set(answer_words)
                return

    def get_question_answers(
        self, question_pair: LanguagePair
    ) -> List[Word]:
        answers = [question_pair.russian_word]
        for _ in range(ANSWERS_PER_QUESTION - 1):
            answers.append(self.get_wrong_answer(answers))
        shuffle(answers)
        return answers

    def get_wrong_answer(self, existing_answers: List[Word]) -> Word:
        while True:
            random_language_pair = self.get_random_language_pair()
            if random_language_pair.russian_word not in existing_answers:
                return random_language_pair.russian_word
