from django.db import models
from django.utils import timezone
from django_lifecycle import hook, LifecycleModel, AFTER_UPDATE

from game.models import AppUser


class Game(LifecycleModel):
    game_definition = models.ForeignKey(
        "GameDefinition", on_delete=models.CASCADE, blank=False, null=True
    )
    player = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(blank=False, editable=False)

    @property
    def finished(self):
        return not self.questions.filter(
            selected_answer="",
        ).exists()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.pk:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Player {str(self.player)} - points {self.points}"

    @hook(AFTER_UPDATE, when="points", was=0, is_not=0)
    def update_user_score(self):
        self.player.score += self.points
        self.player.save()
