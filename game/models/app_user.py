from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    vk_id = models.PositiveBigIntegerField(
        default=0, verbose_name="VK ID", unique=True
    )
    score = models.PositiveIntegerField(
        default=0, verbose_name="Счет", blank=True
    )
    visits_number = models.PositiveIntegerField(
        default=1, verbose_name="Количество визитов"
    )

    @property
    def games_number(self):
        return self.game_set.count()

    @property
    def completed_games_number(self):
        return self.game_set.filter(points__gt=0).count()

    def __str__(self):
        return str(self.vk_id)
