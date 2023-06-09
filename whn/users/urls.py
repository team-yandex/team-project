from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView
from django.urls import path
from django.urls import register_converter

from users import converter
from users import views


register_converter(converter.PositiveIntegerConverter, 'PosIntConv')

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        views.CustomLoginView.as_view(
            template_name='users/login.html',
        ),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(
            template_name='users/logged_out.html',
        ),
        name='logout',
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path(
        'sign_up/',
        views.SignUpView.as_view(),
        name='sign_up',
    ),
    path(
        'activate/<str:username>/',
        views.Activate.as_view(),
        name='activate',
    ),
    path(
        'leaderboard/',
        views.LeaderBoard.as_view(),
        name='leaderboard',
    ),
    path(
        'user_detail/<PosIntConv:pk>/',
        views.UserDetail.as_view(),
        name='user_detail',
    ),
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile',
    ),
]
