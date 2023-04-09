from django.urls import path
from django.views.generic import TemplateView


app_name = 'info'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(
            template_name='base.html'
        ),
        name='index_page'
    ),
]
