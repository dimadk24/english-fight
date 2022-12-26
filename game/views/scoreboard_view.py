from enum import Enum

from django.db.models import Sum, Q, Count
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView

from game.constants import SCOREBOARD_LIMIT
from game.models import AppUser
from game.serializers.scoreboard_user_serializer import (
    ForeverScoreboardUserSerializer,
    MonthlyScoreboardUserSerializer,
)


class ScoreboardType(Enum):
    monthly = "monthly"
    forever = "forever"


class ScoreboardView(ListAPIView):
    type = None

    def get_serializer_class(self):
        if self.type == ScoreboardType.monthly:
            return MonthlyScoreboardUserSerializer
        if self.type == ScoreboardType.forever:
            return ForeverScoreboardUserSerializer
        raise APIException(f"Invalid type: '{self.type}'")

    def get_queryset(self):
        qs = AppUser.users.filter(score__gt=0).annotate(Count("game"))

        if self.type == ScoreboardType.monthly:
            current_month = timezone.now().month
            monthly_score = Sum(
                "game__points", filter=Q(game__created_at__month=current_month)
            )
            return (
                qs.annotate(monthly_score=monthly_score)
                .filter(monthly_score__gt=0)
                .order_by("-monthly_score", "game__count", "vk_id")
                .defer("score")[:SCOREBOARD_LIMIT]
            )
        if self.type == ScoreboardType.forever:
            return qs.order_by("-score", "game__count", "vk_id")[
                :SCOREBOARD_LIMIT
            ]
        raise APIException(f"Invalid type: '{self.type}'")
