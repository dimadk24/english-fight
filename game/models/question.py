from django.db import models
from django.db.models import F
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE

from game.constants import QUESTIONS_PER_GAME
from game.game_utils import get_score_for_game
from json_encoder import UnicodeJSONEncoder


class Question(LifecycleModel):
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="questions"
    )
    question_word = models.CharField(max_length=50, blank=False)
    answer_words = models.JSONField(
        default=list, blank=False, encoder=UnicodeJSONEncoder
    )
    correct_answer = models.CharField(max_length=50, blank=False)
    selected_answer = models.CharField(max_length=50, blank=True, default="")

    @property
    def is_correct(self) -> bool:
        return self.selected_answer == self.correct_answer

    def __str__(self):
        return (
            f"{self.question_word} - {self.correct_answer}; "
            f"selected - {self.selected_answer}"
        )

    @hook(AFTER_UPDATE, when="selected_answer", was="", is_not="")
    def update_game_score(self):
        number_of_not_completed_questions_in_game = self.game.questions.filter(
            selected_answer="",
        ).count()
        if number_of_not_completed_questions_in_game == 0:
            correct_questions_number = self.game.questions.filter(
                selected_answer=F("correct_answer")
            ).count()
            incorrect_questions_number = (
                QUESTIONS_PER_GAME - correct_questions_number
            )
            self.game.points = get_score_for_game(
                correct_questions_number, incorrect_questions_number
            )
            self.game.save()
