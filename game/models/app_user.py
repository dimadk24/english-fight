from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
from django.db import models


class AppUser(AbstractUser):
    vk_id = models.PositiveBigIntegerField(
        default=0, verbose_name="VK ID", unique=True
    )
    score = models.PositiveIntegerField(
        default=0, verbose_name="Счет", blank=True
    )
    # VK has photo urls that have length 230 and more,
    # for MySQL CharField max is 250.
    # Thus it's safer to use TextField
    photo_url = models.TextField(
        default="",
        verbose_name="Photo URL",
        validators=[URLValidator(schemes=("http", "https"))],
        blank=True,
    )

    @property
    def games_number(self):
        return self.game_set.count()

    @property
    def completed_games_number(self):
        return self.game_set.filter(points__gt=0).count()

    def __str__(self):
        return self.username
