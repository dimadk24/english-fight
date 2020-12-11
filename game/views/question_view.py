from rest_framework.generics import UpdateAPIView

from game.models import Question
from game.permissions import OwnQuestionPermission
from game.serializers.question_with_answer_serializer import \
    QuestionWithAnswerSerializer


class QuestionView(UpdateAPIView):
    serializer_class = QuestionWithAnswerSerializer
    permission_classes = [OwnQuestionPermission]

    def get_queryset(self):
        return Question.objects.filter(
            game__player=self.request.user
        ).select_related('game__player')
