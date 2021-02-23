from game.consumers import BaseGameConsumer, AuthenticateGameConsumerMixin


class MultiplayerGameConsumer(BaseGameConsumer, AuthenticateGameConsumerMixin):
    pass
