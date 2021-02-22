from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from game.models import GameDefinition
from game.serializers.game_definition_serializer import (
    GameDefinitionSerializer,
)


class GameDefinitionView(CreateAPIView, RetrieveAPIView):
    serializer_class = GameDefinitionSerializer
    queryset = GameDefinition.objects.all()

    def get_object(self):
        instance = super().get_object()
        if instance.started:
            raise PermissionDenied(detail='К игре уже нельзя подключиться')
        return instance
