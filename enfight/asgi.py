"""
ASGI config for enfight project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import game.websocket_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enfight.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(game.websocket_urls.websocket_urlpatterns),
    }
)
