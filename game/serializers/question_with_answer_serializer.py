from rest_framework import serializers

from game.models import Word
from game.serializers.question_serializer import QuestionSerializer


class QuestionWithAnswerSerializer(QuestionSerializer):
    correct_answer = serializers.SlugRelatedField(slug_field='text',
                                                  queryset=Word.objects.all())
