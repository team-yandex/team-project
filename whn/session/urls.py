from django.urls import path
from session.views import (
    ConnectSessionView,
    CreateSessionView,
    LobbyView,
    QuestionView,
)


app_name = 'session'

urlpatterns = [
    path('create/', CreateSessionView.as_view(), name='create'),
    path('connect/', ConnectSessionView.as_view(), name='connect'),
    path('lobby/', LobbyView.as_view(), name='lobby'),
    path(
        'question/<int:pk>/',
        QuestionView.as_view(),
        name='question',
    ),
]
