from django.db import models
from django.db.models import F
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE

from common.json_encoder import UnicodeJSONEncoder
from game.game_utils import GameUtils


class Question(LifecycleModel):
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=255, blank=False)
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
            f"{self.question} - {self.correct_answer}; "
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
            self.game.points = GameUtils.get_score_for_game(
                correct_questions_number
            )
            self.game.save()
