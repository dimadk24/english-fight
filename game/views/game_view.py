from django.db import transaction
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from game.game_questions_creators.word_questions_creator import (
    create_word_questions,
)
from game.models import Game
from game.serializers.game_serializer import GameSerializer


class GameView(CreateAPIView, RetrieveAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(player=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer: GameSerializer):
        serializer.save()
        create_word_questions(serializer.instance)
