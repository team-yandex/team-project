from django.urls import re_path

import game.consumers


websocket_urlpatterns = [
    re_path(
        r'ws/question/(?P<question_id>\w+)/$',
        game.consumers.QuestionConsumer.as_asgi(),
    ),
]
