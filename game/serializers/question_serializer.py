from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from game.models import Question


class QuestionSerializer(FlexFieldsModelSerializer):
    correct_answer = serializers.SerializerMethodField()
    is_correct = serializers.BooleanField(read_only=True)

    def get_correct_answer(self, obj):
        # Don't include correct answer when create and return game.
        # Answer is included in QuestionWithAnswerSerializer
        return None

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "answer_words",
            "correct_answer",
            "selected_answer",
            "is_correct",
        )
