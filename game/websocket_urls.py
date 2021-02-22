from django.urls import re_path

from game.multiplayer_game_consumer import MultiplayerGameConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/multiplayer-game/(?P<game_def_id>\w+)$',
        MultiplayerGameConsumer.as_asgi(),
    ),
]
