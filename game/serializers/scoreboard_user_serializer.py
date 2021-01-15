from rest_framework import serializers

from game.models import AppUser


class ForeverScoreboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = (
            "id",
            "score",
            "first_name",
            "last_name",
            "photo_url",
        )


class MonthlyScoreboardUserSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    class Meta:
        model = AppUser
        fields = (
            "id",
            "score",
            "first_name",
            "last_name",
            "photo_url",
        )

    def get_score(self, obj):
        return obj.monthly_score
