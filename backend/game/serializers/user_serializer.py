from django.db.models import Q, Sum, Count
from django.utils import timezone
from rest_framework import serializers

from game.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    monthly_score = serializers.SerializerMethodField()
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
            "monthly_score",
            "forever_rank",
            "monthly_rank",
            "notifications_status",
        )
        read_only_fields = (
            "id",
            "vk_id",
            "first_name",
            "last_name",
            "photo_url",
            "score",
            "monthly_score",
            "forever_rank",
            "monthly_rank",
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

    def annotate_users_with_monthly_score(self):
        current_month = timezone.now().month
        monthly_score_annotation = Sum(
            "game__points", filter=Q(game__created_at__month=current_month)
        )
        return AppUser.users.annotate(Count("game")).annotate(
            monthly_score=monthly_score_annotation
        )

    def get_monthly_rank(self, user: AppUser):
        annotated_users = self.annotate_users_with_monthly_score()
        user_games_count = user.game_set.count()
        user_monthly_score = self.get_monthly_score(user)
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

    def get_monthly_score(self, user: AppUser):
        return (
            self.annotate_users_with_monthly_score()
            .get(vk_id=user.vk_id)
            .monthly_score
            or 0
        )
