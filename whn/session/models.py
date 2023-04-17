from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    IntegerChoices,
    ManyToManyField,
    Model,
    PositiveSmallIntegerField,
    TextChoices,
    UUIDField,
)

from users.models import User


class Session(Model):
    code = UUIDField(
        'код', help_text='код сессии', max_length=200, default=uuid4
    )

    max_users = PositiveSmallIntegerField(
        'максимум игроков',
        help_text='максимум игроков',
        validators=[
            MinValueValidator(2),
            MaxValueValidator(10),
        ],
    )

    class Status(TextChoices):
        UPCOMING = 'upcoming', 'не началась'
        ACTIVE = 'active', 'идёт'
        ENDED = 'ended', 'окончена'

    status = CharField(
        'статус',
        help_text='статус комнаты',
        choices=Status.choices,
        default=Status.UPCOMING,
        max_length=15,
    )

    class Complexity(IntegerChoices):
        EASY = 1, 'легко'
        MEDIUM = 2, 'средне'
        HARD = 3, 'тяжело'

    complexity = PositiveSmallIntegerField(
        'сложность',
        help_text='сложность заданий в сессии',
        choices=Complexity.choices,
    )

    max_questions = PositiveSmallIntegerField(
        'всего вопросов',
        help_text='количество вопросов в сессии',
        validators=[MaxValueValidator(25)],
    )

    owner = ForeignKey(User, on_delete=CASCADE, null=True)

    users = ManyToManyField(User, 'пользователи')

    def __str__(self):
        return str(self.id)
