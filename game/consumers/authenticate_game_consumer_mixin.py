from asgiref.sync import async_to_sync
from rest_framework.exceptions import AuthenticationFailed
from typing_extensions import TypedDict

from game.authentication.websocket_authentication import authenticate_websocket
from game.consumers.base_game_consumer import (
    BaseGameConsumer,
    Scope,
)
from game.models import GameDefinition
from game.serializers.game_definition_serializer import (
    GameDefinitionSerializer,
)


class InputData(TypedDict):
    authorization: str


class AuthenticateGameConsumerMixin:
    scope: Scope

    def authenticate(self, data: InputData):
        authorization = data['authorization']
        if not authorization:
            raise AuthenticationFailed(
                'You should provide authorization param to authenticate event'
            )
        user = authenticate_websocket(authorization)
        self.scope['user'] = user
        self.on_authenticate()

    def on_authenticate(self: BaseGameConsumer):
        game_def = GameDefinition.objects.get(id=self.scope['game_def_id'])
        game_def.players.add(self.scope['user'])
        serialized_instance = GameDefinitionSerializer(game_def).data
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'send_joined_game', 'object': serialized_instance},
        )

    def send_joined_game(self: BaseGameConsumer, data: dict):
        self.send_json(
            {
                'type': 'joined-game',
                'model': 'game_definition',
                'instance': data['object'],
            }
        )
