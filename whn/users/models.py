from django.contrib.auth.models import AbstractUser
from django.db import models
from django_cleanup.signals import cleanup_pre_delete
import sorl
from sorl.thumbnail import delete, get_thumbnail

# from game.models import Question
from .managers import UserManager


class User(AbstractUser):
    image = sorl.thumbnail.ImageField(
        'аватарка',
        upload_to='media/%Y/%m/',
        blank=True,
        null=True,
        help_text=(
            'По аватарке другие люди смогут вас узнавать, '
            'а вам будет проще определять, в какой аккаунт вы вошли.'
        ),
    )
    score = models.PositiveIntegerField(
        'очки',
        default=0,
        help_text='Количество очков.',
    )

    seen_questions = models.ManyToManyField(
        'game.Question', verbose_name='пройденные вопросы'
    )

    session_points = models.PositiveSmallIntegerField(
        'баллы в сессии', default=0
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    objects = UserManager()

    @property
    def get_image_300x300(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def sorl_delete(**kwargs):
        delete(kwargs['file'])

    cleanup_pre_delete.connect(sorl_delete)

    def __str__(self):
        return self.get_username()
