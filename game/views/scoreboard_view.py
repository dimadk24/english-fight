from rest_framework.generics import ListAPIView

from game.constants import SCOREBOARD_LIMIT
from game.models import AppUser
from game.serializers.scoreboard_user_serializer import (
    ScoreboardUserSerializer,
)


class ScoreboardView(ListAPIView):
    serializer_class = ScoreboardUserSerializer

    def get_queryset(self):
        return AppUser.objects.filter(
            is_staff=False, is_active=True, is_superuser=False, score__gt=0
        ).order_by("-score")[:SCOREBOARD_LIMIT]
