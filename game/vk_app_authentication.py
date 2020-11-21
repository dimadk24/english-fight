from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from django.conf import settings
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from game.models import AppUser


class VKAppAuthentication(BaseAuthentication):
    def authenticate(self, request: HttpRequest):
        authorization_header: str = request.headers.get('Authorization', '')
        if not authorization_header:
            return None
        if not authorization_header.startswith('QueryString '):
            return None
        auth_query_params = authorization_header.split(' ')[1]

        query_params_dict = dict(parse_qsl(auth_query_params,
                                           keep_blank_values=True))
        result = VKAppAuthentication.is_valid_vk_query(query_params_dict,
                                                       settings.VK_SECRET)
        if not result:
            raise AuthenticationFailed('Incorrect VK query string.')
        vk_user_id = query_params_dict['vk_user_id']
        try:
            user = AppUser.objects.get(vk_id=vk_user_id)
        except AppUser.DoesNotExist:
            user = AppUser.objects.create(
                vk_id=vk_user_id,
                username=vk_user_id)
        return user, query_params_dict

    @staticmethod
    def is_valid_vk_query(query_params: dict, secret: str) -> bool:
        """
        Check VK Apps signature
        Adapted from https://vk.com/dev/vk_apps_launch_params
        """
        vk_params = OrderedDict(
            sorted(x for x in query_params.items() if x[0][:3] == "vk_"))
        hash_code = b64encode(
            HMAC(secret.encode(),
                 urlencode(vk_params, doseq=True).encode(),
                 sha256).digest())
        decoded_hash_code = hash_code.decode('utf-8')[:-1] \
            .replace('+', '-') \
            .replace('/', '_')
        return query_params["sign"] == decoded_hash_code
