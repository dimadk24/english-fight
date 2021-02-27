from game.consumers import BaseGameConsumer, AuthenticateGameConsumerMixin
from game.consumers.start_game_consumer_mixin import StartGameConsumerMixin


class MultiplayerGameConsumer(
    BaseGameConsumer,
    AuthenticateGameConsumerMixin,
    StartGameConsumerMixin,
):
    pass
