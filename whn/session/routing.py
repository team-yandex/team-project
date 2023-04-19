from django.urls import re_path

import session.consumers


websocket_urlpatterns = [
    re_path(
        # dot may be a weak place of regexp
        r'ws/room/(?P<session_id>.+)/$',
        session.consumers.LobbyConsumer.as_asgi(),
    ),
]
