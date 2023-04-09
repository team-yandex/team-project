from django.urls import path
from info.views import AboutView, IndexView


app_name = 'info'

urlpatterns = [
    path('', IndexView.as_view(), name='index_page'),
    path('about/', AboutView.as_view(), name='about_page'),
]
