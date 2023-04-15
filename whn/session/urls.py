from django.urls import path
from session.views import CreateSessionView, LobbyView


app_name = 'session'

urlpatterns = [
    path('create/', CreateSessionView.as_view(), name='create'),
    path('lobby/', LobbyView.as_view(), name='lobby'),
]
