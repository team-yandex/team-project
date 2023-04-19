from django import forms

from core.forms import BootstrapFormMixin
from feedback.models import Feedback
from feedback.models import FeedbackAuther
from feedback.models import FeedbackFile


class FeedbackAutherForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FeedbackAuther
        fields = (
            model.name.field.name,
            model.email.field.name,
        )
        labels = {
            model.name.field.name: 'Имя',
            model.email.field.name: 'Контактная электронная почта',
        }
        help_texts = {
            model.email.field.name: 'На этот адрес будет отправлен ответ',
        }
        widgets = {
            model.email.field.name: forms.EmailInput(
                attrs={'placeholder': 'default@example.com'}
            )
        }


class FeedbackFileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FeedbackFile
        fields = (model.file.field.name,)
        help_texts = {
            model.file.field.name: 'При необходимости прикрепите файлы',
        }
        widgets = {
            model.file.field.name: forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'type': 'file',
                    'multiple': True,
                }
            )
        }


class FeedbackForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (model.text.field.name,)
        labels = {
            model.text.field.name: 'Текст сообщения',
        }
