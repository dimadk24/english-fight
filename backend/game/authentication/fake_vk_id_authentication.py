from django.contrib.auth.models import update_last_login
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication

from game.authentication.authentication_utils import (
    get_auth_header,
    get_auth_value,
    set_user_data,
)
from game.authentication.base_websocket_authentication import (
    AbstractWebsocketAuthentication,
)
from game.models import AppUser


class FakeVKIDAuthentication(
    BaseAuthentication,
    AbstractWebsocketAuthentication,
):
    @get_auth_header
    def authenticate(self, request: HttpRequest, auth_header: str):
        return self.authenticate_auth_header(auth_header=auth_header)

    @get_auth_value('FakeVKID')
    def authenticate_auth_header(self, *, auth_header: str, auth_value: str):
        fake_vk_id = int(auth_value)
        user, _ = AppUser.objects.get_or_create(
            vk_id=fake_vk_id, defaults={'username': fake_vk_id}
        )
        update_last_login(None, user)
        set_user_data(user)
        return user, fake_vk_id
