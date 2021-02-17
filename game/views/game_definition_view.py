from rest_framework.generics import CreateAPIView, RetrieveAPIView

from game.models import GameDefinition
from game.serializers.game_definition_serializer import (
    GameDefinitionSerializer,
)


class GameDefinitionView(CreateAPIView, RetrieveAPIView):
    serializer_class = GameDefinitionSerializer
    queryset = GameDefinition.objects.all()
