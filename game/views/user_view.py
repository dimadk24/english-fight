from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework.generics import RetrieveAPIView

from game.models import AppUser
from game.serializers.user_serializer import UserSerializer


class UsersView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
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
        current_month = timezone.now().month
        monthly_score = Sum(
            "game__points", filter=Q(game__created_at__month=current_month)
        )
        annotated_users = annotated_users.annotate(monthly_score=monthly_score)
        user_monthly_score = annotated_users.get(
            vk_id=user.vk_id
        ).monthly_score
        monthly_rank = (
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
        return {
            "id": user.id,
            "score": user.score,
            "vk_id": user.vk_id,
            "forever_rank": forever_rank,
            "monthly_rank": monthly_rank,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo_url": user.photo_url,
        }
