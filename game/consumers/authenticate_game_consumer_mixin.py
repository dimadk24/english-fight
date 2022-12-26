from asgiref.sync import async_to_sync
from rest_framework.exceptions import AuthenticationFailed
from typing_extensions import TypedDict

from game.authentication.websocket_authentication import authenticate_websocket
from game.consumers.base_game_consumer import (
    BaseGameConsumer,
    Scope,
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
        self.scope['game_def'].players.add(self.scope['user'])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'send_joined_game'},
        )

    def send_joined_game(self: BaseGameConsumer, data: dict):
        self.send_data('joined-game', self.scope['game_def'])
