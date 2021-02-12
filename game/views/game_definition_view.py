from rest_framework.generics import CreateAPIView, RetrieveAPIView

from game.models import GameDefinition
from game.serializers.game_definition_serializer import (
    GameDefinitionSerializer,
)


class GameDefinitionView(CreateAPIView, RetrieveAPIView):
    serializer_class = GameDefinitionSerializer

    def get_queryset(self):
        return GameDefinition.objects.filter(
            players__contains=self.request.user
        )
