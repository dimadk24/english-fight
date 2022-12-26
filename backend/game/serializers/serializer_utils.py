from typing import Type

from rest_framework.serializers import ModelSerializer

from game.serializers.game_definition_serializer import (
    GameDefinitionSerializer,
)
from game.serializers.game_serializer import GameSerializer
from game.serializers.question_serializer import QuestionSerializer
from game.serializers.user_serializer import UserSerializer

serializers_by_template_name = {
    'game_definition': GameDefinitionSerializer,
    'game': GameSerializer,
    'question': QuestionSerializer,
    'user': UserSerializer,
}


def get_serializer_by_model_name(
    model_name: str,
) -> Type[ModelSerializer]:
    if model_name not in serializers_by_template_name:
        raise Exception(
            f'There is no predefined serializer with model name "{model_name}"'
        )
    return serializers_by_template_name[model_name]
