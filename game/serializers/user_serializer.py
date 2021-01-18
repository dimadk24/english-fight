from rest_framework import serializers

from game.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    forever_rank = serializers.IntegerField()
    monthly_rank = serializers.IntegerField()

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
        )
