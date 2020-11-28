from django.db import models
from django.utils import timezone

from game.models import Word


class LanguagePair(models.Model):
    russian_word = models.OneToOneField(Word, on_delete=models.CASCADE,
                                        unique=True, blank=False,
                                        related_name='russian_pair')
    english_word = models.OneToOneField(Word, on_delete=models.CASCADE,
                                        unique=True, blank=False,
                                        related_name='english_pair')
    created_at = models.DateTimeField(blank=False, editable=False)
    visible = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.pk:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.russian_word} - {self.english_word}'
