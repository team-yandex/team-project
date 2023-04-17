import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application
import session.routing

import game.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whn.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    game.routing.websocket_urlpatterns
                    + session.routing.websocket_urlpatterns
                )
            ),
        ),
    }
)
