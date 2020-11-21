from rest_framework.generics import RetrieveAPIView

from game.serializers.user_serializer import UserSerializer


class UsersView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
