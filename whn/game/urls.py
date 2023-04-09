import django.urls

import game.views


app_name = 'game'

urlpatterns = [
    django.urls.path(
        'question/<int:pk>',  # TODO: random question
        game.views.QuestionView.as_view(),
        name='question',
    ),
    django.urls.path(
        'result/', game.views.ResultView.as_view(), name='result'
    ),
]
