from hashid_field.rest import HashidSerializerCharField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from game.models import GameDefinition, AppUser
from game.serializers.user_serializer import UserSerializer

queryset = AppUser.objects.all()


class GameDefinitionSerializer(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(
        source_field="game.GameDefinition.id",
        read_only=True,
    )
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    players = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def save(self, **kwargs):
        creator = self.context["request"].user
        kwargs["creator"] = creator
        return super().save(**kwargs)

    class Meta:
        model = GameDefinition
        fields = ["id", "creator", "players", "type"]
        expandable_fields = {
            "creator": UserSerializer,
            "players": (UserSerializer, {"many": True}),
        }
