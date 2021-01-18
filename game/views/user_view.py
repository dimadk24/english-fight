from rest_framework.generics import RetrieveAPIView

from game.models import AppUser
from game.serializers.user_serializer import UserSerializer


class UsersView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        rank = (
            AppUser.objects.filter(
                score__gt=user.score,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            ).count()
            + 1
        )
        return {
            "id": user.id,
            "score": user.score,
            "vk_id": user.vk_id,
            "rank": rank,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo_url": user.photo_url,
        }
