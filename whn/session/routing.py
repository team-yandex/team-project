from django.urls import re_path
import session.consumers


websocket_urlpatterns = [
    re_path(
        r'ws/room/(?P<session_id\w+)/$',
        session.consumers.LobbyConsumer.as_asgi(),
    ),
]
