from django.db import models

from game.models import Word


class Question(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE,
                             related_name='questions')
    question_word = models.ForeignKey(Word, on_delete=models.CASCADE,
                                      related_name='questions_with_question')
    answer_words = models.ManyToManyField(Word,
                                          related_name='questions_with_answers')
    correct_answer = models.ForeignKey(
        Word, on_delete=models.CASCADE,
        related_name='questions_with_correct_answer')
    selected_answer = models.ForeignKey(
        Word, on_delete=models.CASCADE,
        related_name='questions_with_selected_answer',
        null=True, blank=True)

    @property
    def is_correct(self) -> bool:
        return self.selected_answer == self.correct_answer

    def __str__(self):
        return (
            f'{self.question_word} - {self.correct_answer}; '
            f'selected - {self.selected_answer}'
        )
