from hashid_field.rest import HashidSerializerCharField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from game.models import Game, GameDefinition
from game.serializers.game_definition_serializer import (
    GameDefinitionSerializer,
)
from game.serializers.question_serializer import QuestionSerializer


class GameSerializer(FlexFieldsModelSerializer):
    player = serializers.HiddenField(default=CurrentUserDefault())
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    game_definition = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(
            source_field="game.GameDefinition.id",
            read_only=True,
        ),
        queryset=GameDefinition.objects.all(),
    )

    class Meta:
        model = Game
        fields = ["id", "player", "questions", "points", "game_definition"]
        expandable_fields = {
            "questions": (QuestionSerializer, {"many": True}),
            "game_definition": (GameDefinitionSerializer, {"many": True}),
        }
