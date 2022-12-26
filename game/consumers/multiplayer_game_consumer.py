from game.consumers import BaseGameConsumer, AuthenticateGameConsumerMixin
from game.consumers.finished_game_consumer_mixin import (
    FinishedGameConsumerMixin,
)
from game.consumers.start_game_consumer_mixin import StartGameConsumerMixin


class MultiplayerGameConsumer(
    BaseGameConsumer,
    AuthenticateGameConsumerMixin,
    StartGameConsumerMixin,
    FinishedGameConsumerMixin,
):
    pass
