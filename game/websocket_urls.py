from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        'ws/multiplayer-game$',
        consumers.MultiplayerGameConsumer.as_asgi(),
    ),
]
