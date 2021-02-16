from django.contrib.auth.models import update_last_login
from rest_framework.authentication import BaseAuthentication

from game.authentication_backends.authentication_utils import (
    get_auth_header,
    get_auth_value,
    set_user_data,
)
from game.models import AppUser


class FakeVKIDAuthentication(BaseAuthentication):
    @get_auth_header
    @get_auth_value("FakeVKID")
    def authenticate(self, *args, **kwargs):
        fake_vk_id = int(kwargs["auth_value"])
        user, _ = AppUser.objects.get_or_create(
            vk_id=fake_vk_id, defaults={"username": fake_vk_id}
        )
        update_last_login(None, user)
        set_user_data(user)
        return user, fake_vk_id
