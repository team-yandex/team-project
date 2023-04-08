import django.core.validators
import django.db.models


class Question(django.db.models.Model):
    video = django.db.models.FileField(
        'видео',
        help_text='загрузите видео',
        upload_to='video',
        validators=[
            django.core.validators.FileExtensionValidator(
                allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv']
            )
        ],
    )
    score = django.db.models.PositiveIntegerField(
        'очки',
        help_text='введите очки за данный вопрос',
    )
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    # TODO: author
    # related_name нужно переопределить,
    #  иначе будет ошибка совпадения related полей
    answer = django.db.models.OneToOneField(
        'Choice',
        verbose_name='ответ',
        help_text='выберете вариант, который является ответом',
        on_delete=django.db.models.CASCADE,
        related_name='answered_question',
        null=True,
        blank=True,
    )
    climax_second = django.db.models.PositiveSmallIntegerField(
        'секунда кульминации',
        help_text='введите секунду кульминации',
    )

    class Complexity(django.db.models.IntegerChoices):
        easy = 1, 'легко'
        medium = 2, 'средне'
        hard = 3, 'сложно'

    complexity = django.db.models.PositiveSmallIntegerField(
        'сложность', help_text='введите сложность', choices=Complexity.choices
    )
    is_published = django.db.models.BooleanField(
        'побуликован ли', help_text='укажите опубликоан ли вопрос'
    )
    # TODO: добавить превью видео для админки.

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class Choice(django.db.models.Model):
    label = django.db.models.CharField(
        'текст варианта ответа',
        help_text='введите текст варианта ответа',
        max_length=200,
    )
    question = django.db.models.ForeignKey(
        Question,
        verbose_name='вопрос',
        related_name='choices',
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'вариант'
        verbose_name_plural = 'варианты'

    def __str__(self):
        return self.label[:21]
