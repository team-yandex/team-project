import pathlib

import django.core.files
import django.core.validators
import django.db.models
import moviepy.editor

import game.managers
import game.utils


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
    # TODO: author
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
        # TODO: unique together question + choice

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
        return super().save(force_insert, force_update, using, update_fields)

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
    question = django.db.models.ForeignKey(
        Question,
        verbose_name='вопрос',
        related_name='choices',
        on_delete=django.db.models.CASCADE,
    )
    # TODO: only one correct for question
    is_correct = django.db.models.BooleanField(
        'верный ли',
        help_text='выберете, является ли этот вариант верным',
        default=False,
    )

    class Meta:
        verbose_name = 'вариант'
        verbose_name_plural = 'варианты'

    def __str__(self):
        return self.label[:21]
