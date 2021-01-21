from django.db.models import Q, Sum, Count
from django.utils import timezone
from rest_framework import serializers

from game.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    forever_rank = serializers.SerializerMethodField()
    monthly_rank = serializers.SerializerMethodField()

    class Meta:
        model = AppUser
        fields = (
            "id",
            "vk_id",
            "first_name",
            "last_name",
            "photo_url",
            "score",
            "forever_rank",
            "monthly_rank",
            "notifications_status",
        )

    def get_forever_rank(self, user: AppUser):
        user_games_count = user.game_set.count()
        annotated_users = AppUser.users.annotate(Count("game"))
        forever_rank = (
            annotated_users.filter(score__gt=user.score)
            .union(
                annotated_users.filter(
                    Q(score=user.score) & Q(game__count__lt=user_games_count),
                ),
                annotated_users.filter(
                    Q(score=user.score)
                    & Q(game__count=user_games_count)
                    & Q(vk_id__lt=user.vk_id),
                ),
            )
            .count()
            + 1
        )
        return forever_rank

    def get_monthly_rank(self, user: AppUser):
        current_month = timezone.now().month
        monthly_score = Sum(
            "game__points", filter=Q(game__created_at__month=current_month)
        )
        annotated_users = AppUser.users.annotate(Count("game"))
        annotated_users = annotated_users.annotate(monthly_score=monthly_score)
        user_monthly_score = (
            annotated_users.get(vk_id=user.vk_id).monthly_score or 0
        )
        user_games_count = user.game_set.count()
        return (
            annotated_users.filter(monthly_score__gt=user_monthly_score)
            .union(
                annotated_users.filter(
                    Q(monthly_score=user.score)
                    & Q(game__count__lt=user_games_count),
                ),
                annotated_users.filter(
                    Q(monthly_score=user.score)
                    & Q(game__count=user_games_count)
                    & Q(vk_id__lt=user.vk_id),
                ),
            )
            .count()
            + 1
        )
