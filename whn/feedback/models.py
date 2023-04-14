from django.db import models
from django.utils.datetime_safe import time


class Feedback(models.Model): 
    class Status(models.TextChoices): 
        GET = 'get', 'Получено'
        IN_PROCESSING = 'saw', 'В обработке'
        ANSWERED = 'ans', 'Ответ дан'

    text = models.TextField(
        'текст',
        max_length=200,
        help_text='Максимальная длина 200 символов',
    )
    created_on = models.DateTimeField(
        'дата создания',
        auto_now_add=True,
        help_text='Когда был написан отзыв',
    )
    status = models.CharField(
        'статус обработки',
        max_length=3,
        choices=Status.choices,
        default=Status.GET,
        help_text='Что сейчас происходит с отзывом',
    )


class FeedbackAuther(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        related_name='auther',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'имя',
        max_length=64,
        help_text='Максимальная длина 64 символа',
    )
    email = models.EmailField(
        'почта',
        max_length=254,
        help_text='Максимум 254 символа',
    )


class FeedbackFile(models.Model):
    def get_path(self, filename):
        return f'uploads/{self.feedback_id}/{time()}_{filename}'

    feedback = models.ForeignKey(
        Feedback,
        related_name='files',
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        'файл',
        upload_to=get_path,
        blank=True,
    )




