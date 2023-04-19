from django.urls import path

from session.views import ConnectSessionView
from session.views import CreateSessionView
from session.views import LobbyView
from session.views import QuestionView


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
