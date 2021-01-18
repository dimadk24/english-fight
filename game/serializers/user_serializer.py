from rest_framework import serializers

from game.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField()

    class Meta:
        model = AppUser
        fields = (
            "id",
            "vk_id",
            "first_name",
            "last_name",
            "photo_url",
            "score",
            "rank",
        )
