from asgiref.sync import async_to_sync
from django.utils import timezone

from game.consumers import BaseGameConsumer
from game.consumers.base_game_consumer import Scope
from game.game_questions_creators import create_questions
from game.models import GameDefinition, Game
from game.serializers.game_serializer import GameSerializer


def create_games(game_def: GameDefinition):
    games = [
        Game(
            game_definition=game_def,
            player=player,
            created_at=timezone.now(),
        )
        for player in game_def.players.all()
    ]
    Game.objects.bulk_create(games)
    games = Game.objects.filter(game_definition=game_def)
    for game in games:
        create_questions(game)


class StartGameConsumerMixin:
    scope: Scope

    def start_game(self: BaseGameConsumer, data):
        game_def: GameDefinition = GameDefinition.objects.get(
            id=self.scope['game_def_id']
        )
        game_def.started = True
        game_def.save()
        create_games(game_def)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'send_started_game'}
        )

    def send_started_game(self: BaseGameConsumer, data):
        user_game = Game.objects.get(
            game_definition_id=self.scope['game_def_id'],
            player=self.scope['user'],
        )
        game_data = GameSerializer(user_game).data
        self.send_json(
            {
                'type': 'started-game',
                'model': 'game',
                'instance': game_data,
            }
        )
