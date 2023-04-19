import django.urls

import game.views


app_name = 'game'

urlpatterns = [
    django.urls.path(
        'question/',
        game.views.QuestionView.as_view(),
        name='question',
    ),
    django.urls.path(
        'result/', game.views.ResultView.as_view(), name='result'
    ),
    django.urls.path(
        'single/', game.views.SingleView.as_view(), name='single'
    ),
]
