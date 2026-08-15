"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.asgi import get_asgi_application
django_asgi_app=get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from logic.routing import url_patterns
from logic.middleware import JwtAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': JwtAuthMiddleware(URLRouter(url_patterns)),
    'http': django_asgi_app
})
