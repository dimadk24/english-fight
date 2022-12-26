from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.exceptions import AuthenticationFailed

from game.authentication.base_websocket_authentication import (
    AbstractWebsocketAuthentication,
)
from game.models import AppUser


def authenticate_websocket(auth_header: str) -> AppUser:
    """Acts like authentication backends in Django.
    Takes auth string from websocket authentication event
    Returns AppUser instance or raises AuthenticationFailed
    """
    for AuthClassString in settings.WEBSOCKET_AUTHENTICATION_CLASSES:
        AuthClass = import_string(AuthClassString)
        auth_instance: AbstractWebsocketAuthentication = AuthClass()
        response = auth_instance.authenticate_auth_header(
            auth_header=auth_header
        )
        if response:
            return response[0]
    raise AuthenticationFailed(
        'No suitable AUTHENTICATION_CLASS to authenticate '
        f'auth header "{auth_header}"'
    )
