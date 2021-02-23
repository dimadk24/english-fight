from typing import Optional

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from typing_extensions import TypedDict

from game.models import AppUser

AUTH_FAILED_ERROR = 3000


class InputContent(TypedDict):
    type: str
    data: Optional[dict]


class Scope(TypedDict):
    user: AppUser
    game_def_id: str
    url_route: dict


class BaseGameConsumer(JsonWebsocketConsumer):
    scope: Scope

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
        if not self.scope.get('user') and event_type != 'authenticate':
            return self.close(AUTH_FAILED_ERROR)
        method_name = event_type.replace('-', '_')
        method = getattr(self, method_name)
        event_data = content.get('data')
        method(event_data)
