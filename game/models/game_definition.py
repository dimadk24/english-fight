from django.db import models
from django.utils import timezone
from django_lifecycle import LifecycleModel, hook, BEFORE_SAVE
from hashid_field import HashidAutoField

from game.models import AppUser


class GameDefinition(LifecycleModel):
    id = HashidAutoField(primary_key=True)
    creator = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="created_games"
    )
    players = models.ManyToManyField(AppUser, related_name="played_games")
    WORD = "word"
    PICTURE = "picture"
    TYPES = [
        (WORD, WORD),
        (PICTURE, PICTURE),
    ]
    type = models.CharField(choices=TYPES, default=WORD, max_length=30)
    created_at = models.DateTimeField(blank=False, editable=False)

    @hook(BEFORE_SAVE, when="created_at", is_now=None)
    def set_created_at(self):
        self.created_at = timezone.now()

    def __str__(self):
        return f"{self.pk} - type {self.type} - creator {self.creator}"
