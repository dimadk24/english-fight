from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager,
)
from django.core.validators import URLValidator
from django.db import models


class AppUserManager(DjangoUserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_active=True, is_staff=False, is_superuser=False)
        )


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
    ALLOW = "allow"
    BLOCK = "block"
    TO_BE_REQUESTED = "to be requested"
    NOTIFICATIONS_STATUSES = [
        (TO_BE_REQUESTED, TO_BE_REQUESTED),
        (ALLOW, ALLOW),
        (BLOCK, BLOCK),
    ]
    notifications_status = models.CharField(
        max_length=50, choices=NOTIFICATIONS_STATUSES, default=TO_BE_REQUESTED
    )

    objects = DjangoUserManager()
    users = AppUserManager()

    @property
    def games_number(self):
        return self.game_set.count()

    @property
    def completed_games_number(self):
        return self.game_set.filter(points__gt=0).count()

    def __str__(self):
        return str(self.username)
