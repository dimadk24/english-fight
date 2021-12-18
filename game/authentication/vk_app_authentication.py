from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from typing import Dict, Tuple
from urllib.parse import parse_qsl, urlencode

from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from game.authentication.authentication_utils import (
    get_auth_header,
    get_auth_value,
    set_user_data,
)
from game.authentication.base_websocket_authentication import (
    AbstractWebsocketAuthentication,
)
from game.models import AppUser


class VKAppAuthentication(BaseAuthentication, AbstractWebsocketAuthentication):
    @get_auth_header
    def authenticate(self, request: HttpRequest, auth_header: str):
        return self.authenticate_auth_header(auth_header=auth_header)

    @get_auth_value("QueryString")
    def authenticate_auth_header(
        self,
        *,
        auth_header: str,
        auth_value: str,
    ) -> Tuple[AppUser, Dict[str, str]]:
        query_params_dict = dict(parse_qsl(auth_value, keep_blank_values=True))
        is_valid = VKAppAuthentication.is_valid_vk_query(
            query_params_dict, settings.VK_SECRET
        )
        if not is_valid:
            raise AuthenticationFailed("Неверная строка запроса VK")
        vk_user_id = int(query_params_dict["vk_user_id"])

        if not self.is_user_allowed(vk_user_id):
            raise AuthenticationFailed("У вас нет доступа к приложению")
        user, _ = AppUser.objects.get_or_create(  # type: ignore
            vk_id=vk_user_id, defaults={"username": vk_user_id}
        )
        update_last_login(None, user)  # type: ignore
        set_user_data(user)
        return user, query_params_dict

    @staticmethod
    def is_valid_vk_query(query_params: dict, secret: str) -> bool:
        """
        Check VK Apps signature
        Adapted from https://vk.com/dev/vk_apps_launch_params
        """
        vk_params = OrderedDict(
            sorted(x for x in query_params.items() if x[0][:3] == "vk_")
        )
        hash_code = b64encode(
            HMAC(
                secret.encode(),
                urlencode(vk_params, doseq=True).encode(),
                sha256,
            ).digest()
        )
        decoded_hash_code = (
            hash_code.decode("utf-8")[:-1].replace("+", "-").replace("/", "_")
        )
        return query_params["sign"] == decoded_hash_code

    def is_user_allowed(self, user_vk_id: int):
        allow_all_users = settings.VK_ALLOWED_USERS[0] == "*"
        return allow_all_users or user_vk_id in settings.VK_ALLOWED_USERS
