from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
)

from core.forms import BootstrapFormMixin
from .models import User


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
        )
        help_texts = {
            User.email.field.name: 'На этот адрес будет отправлено письмо с '
            'подтверждением.',
        }


class CustomUserChangeForm(BootstrapFormMixin, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[User.score.field.name].disabled = True

    password = None

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            User.email.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.image.field.name,
            User.score.field.name,
        )
