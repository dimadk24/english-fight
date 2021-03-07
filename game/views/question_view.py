from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.generics import UpdateAPIView

from common.list_utils import count_times
from game.models import Question, AppUser
from game.permissions import OwnQuestionPermission
from game.serializers.question_with_answer_serializer import (
    QuestionWithAnswerSerializer,
)


class QuestionView(UpdateAPIView):
    serializer_class = QuestionWithAnswerSerializer
    permission_classes = [OwnQuestionPermission]

    def get_queryset(self):
        return Question.objects.filter(
            game__player=self.request.user
        ).select_related("game__player")

    def perform_update(self, serializer: QuestionWithAnswerSerializer):
        result = super().perform_update(serializer)
        game = serializer.instance.game

        if game.points > 0:
            games_in_game_def = game.game_definition.game_set.count()
            is_multiplayer_game = games_in_game_def > 1
            if is_multiplayer_game:
                channel_layer = get_channel_layer()
                game_def_id = game.game_definition_id
                correct_answers_number = count_times(
                    game.questions.all(), lambda question: question.is_correct
                )
                total_questions = game.questions.count()
                user: AppUser = self.request.user
                async_to_sync(channel_layer.group_send)(
                    f'game-{game_def_id}',
                    {
                        'type': 'send_finished_game',
                        'user_id': user.pk,
                        'points': game.points,
                        'correct_answers_number': correct_answers_number,
                        'total_questions': total_questions,
                    },
                )

        return result
