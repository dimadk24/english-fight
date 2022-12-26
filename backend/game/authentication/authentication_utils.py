from functools import wraps

from django.http import HttpRequest

from game.authentication.authentication_adapter import (
    AuthenticationAdapter,
)
from game.models import AppUser


def get_auth_header(fn):
    @wraps(fn)
    def get_auth_header_wrapper(self, request: HttpRequest, **kwargs):
        authorization_header: str = request.headers.get("Authorization", "")
        if not authorization_header:
            return None
        result = fn(self, request, **kwargs, auth_header=authorization_header)
        return result

    return get_auth_header_wrapper


def get_auth_value(prefix):
    def handler(fn):
        @wraps(fn)
        def get_auth_value_wrapper(*args, **kwargs):
            auth_header = kwargs.get("auth_header")
            if not auth_header:
                raise Exception(
                    "get_auth_value needs auth_header kwarg. "
                    "Add get_auth_header decorator above get_auth_value "
                    "or just pass auth_header as kwarg"
                )
            if not auth_header.startswith(f"{prefix} "):
                return None
            _, auth_value = auth_header.split(" ")
            result = fn(*args, **kwargs, auth_value=auth_value)
            return result

        return get_auth_value_wrapper

    return handler


def set_user_data(user: AppUser):
    if user.photo_url:
        # if photo_url is set, all user vk data is set
        # no need to update it
        return
    user_data = AuthenticationAdapter.get_vk_user_data(user.vk_id)
    user.first_name = user_data["first_name"]
    user.last_name = user_data["last_name"]
    user.photo_url = user_data["photo_200"]
    user.save()
