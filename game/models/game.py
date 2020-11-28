from django.db import models
from django.utils import timezone

from game.models import AppUser


class Game(models.Model):
    player = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(blank=False, editable=False)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.pk:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Player {str(self.player)} - points {self.points}'
