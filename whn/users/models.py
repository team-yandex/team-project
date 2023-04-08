from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import ImageBaseModel
# from game.models import Session
from .managers import UserManager


# class Session(models.Model):
#     pass


class User(ImageBaseModel, AbstractUser):
    image = models.ImageField(
        'аватарка',
        upload_to='media/%Y/%m/',
        blank=True,
        null=True,
        help_text=(
            'По аватарке другие люди смогут вас узнавать, '
            'а вам будет проще определять, в какой аккаунт вы вошли.'
        ),
    )
    score = models.IntegerField(
        'очки',
        default=0,
        help_text='Количество очков.',
    )
    # session_id = models.ForeignKey(
    #     Session,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name='сессия',
    #     help_text='В какой игре сейчас находится пользователь.',
    # )

    # objects = UserManager

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_username()
