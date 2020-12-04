from rest_framework.generics import UpdateAPIView

from game.models import Question
from game.permissions import OwnQuestionPermission
from game.serializers.question_with_answer_serializer import \
    QuestionWithAnswerSerializer


class QuestionView(UpdateAPIView):
    serializer_class = QuestionWithAnswerSerializer
    permission_classes = [OwnQuestionPermission]
    queryset = Question.objects.all()
