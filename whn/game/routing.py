from django.urls import re_path

import game.consumers


websocket_urlpatterns = [
    re_path(
        r'ws/session/(?P<session_id>\w+)/$',
        game.consumers.QuestionConsumer.as_asgi(),
    ),
]
