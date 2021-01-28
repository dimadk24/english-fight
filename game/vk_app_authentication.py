from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import parse_qsl, urlencode

from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from game.models import AppUser
from vk_utils import get_vk_api


class VKAppAuthentication(BaseAuthentication):
    def authenticate(self, request: HttpRequest):
        authorization_header: str = request.headers.get("Authorization", "")
        if not authorization_header:
            return None
        if not authorization_header.startswith("QueryString "):
            return None
        auth_query_params = authorization_header.split(" ")[1]

        query_params_dict = dict(
            parse_qsl(auth_query_params, keep_blank_values=True)
        )
        is_valid = VKAppAuthentication.is_valid_vk_query(
            query_params_dict, settings.VK_SECRET
        )
        if not is_valid:
            raise AuthenticationFailed("Неверная строка запроса VK")
        vk_user_id = int(query_params_dict["vk_user_id"])

        if not self.is_user_allowed(vk_user_id):
            raise AuthenticationFailed("У вас нет доступа к приложению")
        user, _ = AppUser.objects.get_or_create(
            vk_id=vk_user_id, defaults={"username": vk_user_id}
        )
        update_last_login(None, user)
        self.set_user_data(user)
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

    def set_user_data(self, user: AppUser):
        if user.photo_url:
            # if photo_url is set, all user vk data is set
            # no need to update it
            return
        user_data = VKAppAuthentication.get_vk_user_data(user.vk_id)
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.photo_url = user_data["photo_200"]
        user.save()

    @staticmethod
    def get_vk_user_data(vk_id: AppUser):
        return (
            get_vk_api().users.get(
                user_ids=vk_id,
                fields="photo_200,first_name,last_name",
                lang="ru",
            )
        )[0]
