from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from game.models import Question, Word

all_words = Word.objects.all()


class QuestionSerializer(FlexFieldsModelSerializer):
    question_word = serializers.SlugRelatedField(slug_field='text',
                                                 queryset=all_words)
    answer_words = serializers.SlugRelatedField(many=True, slug_field='text',
                                                queryset=all_words)
    correct_answer = serializers.SerializerMethodField()
    selected_answer = serializers.SlugRelatedField(slug_field='text',
                                                   queryset=all_words)
    is_correct = serializers.BooleanField(read_only=True)

    def get_correct_answer(self, obj):
        # Don't include correct answer when create and return game.
        # Answer is included in QuestionWithAnswerSerializer
        return None

    class Meta:
        model = Question
        fields = (
            'id',
            'question_word',
            'answer_words',
            'correct_answer',
            'selected_answer',
            'is_correct',
        )
