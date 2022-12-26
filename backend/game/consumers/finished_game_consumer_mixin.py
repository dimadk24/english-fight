from typing_extensions import TypedDict

from game.consumers.base_game_consumer import (
    BaseGameConsumer,
    Scope,
)
from game.models import AppUser
from game.serializers.scoreboard_user_serializer import (
    ForeverScoreboardUserSerializer,
)


class ReceivedEvent(TypedDict):
    user_id: int
    points: int
    correct_answers_number: int
    total_questions: int


class FinishedGameConsumerMixin:
    scope: Scope

    def send_finished_game(self: BaseGameConsumer, event: ReceivedEvent):
        user = AppUser.objects.get(pk=event['user_id'])
        self.send_data(
            'finished-game',
            instance=user,
            serializer=ForeverScoreboardUserSerializer,
            data={
                'points': event['points'],
                'correct_answers_number': event['correct_answers_number'],
                'total_questions': event['total_questions'],
            },
            model_name='scoreboard_user',
        )
