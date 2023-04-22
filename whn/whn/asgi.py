import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whn.settings')

django_asgi_app = get_asgi_application()


import game.routing  # noqa
import session.routing  # noqa


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
