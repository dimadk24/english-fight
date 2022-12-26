from typing import Optional, Type

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.db.models import Model
from rest_framework.serializers import Serializer
from typing_extensions import TypedDict

from common.string_utils import snake_case
from game.consumers.websocket_errors import (
    AUTH_FAILED_ERROR,
)
from game.models import AppUser, GameDefinition
from game.serializers.serializer_utils import get_serializer_by_model_name


class InputContent(TypedDict):
    type: str
    data: Optional[dict]


class Scope(TypedDict):
    user: AppUser
    game_def_id: str
    game_def: GameDefinition
    url_route: dict


class BaseGameConsumer(JsonWebsocketConsumer):
    scope: Scope

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None

    def connect(self):
        game_def_id = self.scope['url_route']['kwargs']['game_def_id']
        try:
            self.scope['game_def'] = GameDefinition.objects.get(id=game_def_id)
        except GameDefinition.DoesNotExist:
            return self.close()
        if self.scope['game_def'].started:
            return self.close()
        self.scope['game_def_id'] = game_def_id
        self.room_group_name = f'game-{game_def_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        if self.room_group_name:
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
        if not hasattr(self, method_name):
            raise Exception(
                f'received {event_type} event, '
                f'but there is no method {method_name} to handle it'
            )
        method = getattr(self, method_name)
        event_data = content.get('data')
        method(event_data)

    def send_data(
        self,
        event_type: str,
        instance: Optional[Model] = None,
        data: Optional[dict] = None,
        serializer: Optional[Type[Serializer]] = None,
        serializer_kwargs: Optional[dict] = None,
        model_name: Optional[str] = '',
    ):
        data_to_send = {'type': event_type}

        if instance:
            model_name = model_name or snake_case(type(instance).__name__)
            if serializer is None:
                serializer = get_serializer_by_model_name(model_name)
            data_to_send['model'] = model_name
            if serializer_kwargs is None:
                serializer_kwargs = {}
            data_to_send['instance'] = serializer(
                instance, **serializer_kwargs
            ).data

        if data:
            data_to_send['data'] = data

        self.send_json(data_to_send)
