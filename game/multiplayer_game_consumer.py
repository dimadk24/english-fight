from typing import Optional

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.exceptions import AuthenticationFailed
from typing_extensions import TypedDict

from game.authentication.websocket_authentication import authenticate_websocket
from game.models import GameDefinition
from game.serializers.game_definition_serializer import (
    GameDefinitionSerializer,
)

AUTH_FAILED_ERROR = 3000


class JoinGameData(TypedDict):
    id: str


class InputContent(TypedDict):
    type: str
    data: Optional[dict]


class MultiplayerGameConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None

    def connect(self):
        game_def_id = self.scope['url_route']['kwargs']['game_def_id']
        self.scope['game_def_id'] = game_def_id
        self.room_group_name = f'game-{game_def_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive_json(self, content: InputContent, **kwargs):
        event_type = content.get('type')
        if not event_type:
            raise Exception(
                'WS event should include "type" prop. '
                f'Input content: {content}'
            )
        event_data = content.get('data')
        if event_type == 'authenticate':
            return self.authenticate(event_data)
        if not self.scope.get('user'):
            return self.close(AUTH_FAILED_ERROR)
        method_name = event_type.replace('-', '_')
        method = getattr(self, method_name)
        method(event_data)

    def authenticate(self, content):
        authorization = content['authorization']
        if not authorization:
            raise AuthenticationFailed(
                'You should provide authorization param to authenticate event'
            )
        user = authenticate_websocket(authorization)
        self.scope['user'] = user
        self.on_authenticate()

    def on_authenticate(self):
        game_def = GameDefinition.objects.get(id=self.scope['game_def_id'])
        game_def.players.add(self.scope['user'])
        serialized_instance = GameDefinitionSerializer(game_def).data
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'send_joined_game', 'object': serialized_instance},
        )

    def send_joined_game(self, data: dict):
        self.send_json(
            {
                'type': 'joined-game',
                'model': 'game_definition',
                'instance': data['object'],
            }
        )
