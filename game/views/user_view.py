from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from game.serializers.user_serializer import UserSerializer


class UsersView(RetrieveAPIView, UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
