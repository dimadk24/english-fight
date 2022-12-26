from rest_framework import serializers

from game.serializers.question_serializer import QuestionSerializer


class QuestionWithAnswerSerializer(QuestionSerializer):
    correct_answer = serializers.CharField()
