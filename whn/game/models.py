import pathlib

import django.core.exceptions
import django.core.files
import django.core.validators
import django.db.models
import moviepy.editor

import game.managers
import game.utils
import users.models


class Question(django.db.models.Model):
    objects = game.managers.QuestionManager()

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
    author = django.db.models.ForeignKey(
        users.models.User,
        verbose_name='автор',
        help_text='укажите автора вопроса',
        related_name='questions',
        on_delete=django.db.models.CASCADE,
        null=True,
        blank=True,
    )
    climax_second = django.db.models.PositiveSmallIntegerField(
        'секунда кульминации',
        help_text='введите секунду кульминации',
    )
    climax_video = django.db.models.FileField(
        'видео с кульминацией',
        editable=False,
        upload_to='video',
        validators=[
            django.core.validators.FileExtensionValidator(
                allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv']
            )
        ],
    )

    class Complexity(django.db.models.IntegerChoices):
        easy = 1, 'легко'
        medium = 2, 'средне'
        hard = 3, 'сложно'

    complexity = django.db.models.PositiveSmallIntegerField(
        'сложность', help_text='введите сложность', choices=Complexity.choices
    )
    is_published = django.db.models.BooleanField(
        'побуликован ли',
        help_text='укажите опубликоан ли вопрос',
        default=False,
    )
    # TODO: добавить превью видео для админки.

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if (
            update_fields is None
            or Question.climax_video.field.name in update_fields
        ):
            super().save(force_insert, force_update, using, update_fields)
            self.save_climax_video()
        super().save(force_insert, force_update, using, update_fields)
        if self.is_published:
            unique_choices_count = (
                self.choices.values('label_normilized').distinct().count()
            )
            if (
                self.choices.filter(is_correct=True).count() != 1
                or unique_choices_count != 4
            ):
                self.is_published = False
                super().save()

    def save_climax_video(self):
        video_path = pathlib.Path(self.video.path)
        basename, suffix = video_path.stem, video_path.suffix
        climax_filename = f'{basename}_climax{suffix}'
        with django.core.files.temp.NamedTemporaryFile(suffix=suffix) as ntf:
            with moviepy.editor.VideoFileClip(str(video_path)) as video:
                trimmed_video = video.subclip(0, self.climax_second)
                trimmed_video.write_videofile(ntf.name)
                trimmed_video.close()
                self.climax_video.save(
                    climax_filename, django.core.files.File(ntf), save=False
                )


class Choice(django.db.models.Model):
    label = django.db.models.CharField(
        'текст варианта ответа',
        help_text='введите текст варианта ответа',
        max_length=200,
    )
    label_normilized = django.db.models.CharField(
        editable=False,
        max_length=200,
    )
    question = django.db.models.ForeignKey(
        Question,
        verbose_name='вопрос',
        related_name='choices',
        on_delete=django.db.models.CASCADE,
    )
    is_correct = django.db.models.BooleanField(
        'верный ли',
        help_text='выберете, является ли этот вариант верным',
        default=False,
    )

    class Meta:
        verbose_name = 'вариант'
        verbose_name_plural = 'варианты'

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.label_normilized = game.utils.normilize_string(self.label)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.label[:21]
