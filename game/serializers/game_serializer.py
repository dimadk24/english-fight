from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from game.models import Game
from game.serializers.question_serializer import QuestionSerializer


class GameSerializer(FlexFieldsModelSerializer):
    player = serializers.HiddenField(default=CurrentUserDefault())
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ["id", "type", "player", "questions", "points"]
        expandable_fields = {"questions": (QuestionSerializer, {"many": True})}
