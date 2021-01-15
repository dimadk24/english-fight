from enum import Enum

from django.db.models import Sum, Q
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
        assert self.type, "type should be set in forever_scoreboard_url conf"
        if self.type == ScoreboardType.monthly:
            return MonthlyScoreboardUserSerializer
        if self.type == ScoreboardType.forever:
            return ForeverScoreboardUserSerializer
        raise APIException(f"Invalid type: '{self.type}'")

    def get_queryset(self):
        assert self.type, "type should be set in forever_scoreboard_url conf"

        qs = AppUser.objects.filter(
            is_staff=False, is_active=True, is_superuser=False, score__gt=0
        )

        if self.type == ScoreboardType.monthly:
            current_month = timezone.now().month
            monthly_score = Sum(
                "game__points", filter=Q(game__created_at__month=current_month)
            )
            return (
                qs.annotate(monthly_score=monthly_score)
                .filter(monthly_score__gt=0)
                .order_by("-monthly_score")
                .defer("score")[:SCOREBOARD_LIMIT]
            )
        if self.type == ScoreboardType.forever:
            return qs.order_by("-score")[:SCOREBOARD_LIMIT]
        raise APIException(f"Invalid type: '{self.type}'")
