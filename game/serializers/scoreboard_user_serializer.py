from rest_framework import serializers

from game.models import AppUser


class ScoreboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = (
            "id",
            "score",
            "first_name",
            "last_name",
            "photo_url",
        )
