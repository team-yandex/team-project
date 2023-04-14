from django import forms

from core.forms import BootstrapFormMixin
from .models import Feedback, FeedbackAuther, FeedbackFile


class FeedbackAutherForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FeedbackAuther
        fields = (
            FeedbackAuther.name.field.name,
            FeedbackAuther.email.field.name,
        )
        labels = {
            FeedbackAuther.name.field.name: 'Имя',
            FeedbackAuther.email.field.name: 'Контактная электронная почта',
        }
        help_texts = {
            FeedbackAuther.email.field.name: 'На этот адрес будет отправлен ответ',
        }
        widgets = {
            FeedbackAuther.email.field.name: forms.EmailInput(
                attrs={'placeholder': 'default@example.com'}
            )
        }


class FeedbackFileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FeedbackFile
        fields = (
            FeedbackFile.file.field.name,
        )
        help_texts = {
            FeedbackFile.file.field.name: 'При необходимости прикрепите файлы',
        }
        widgets = {
            FeedbackFile.file.field.name: forms.FileInput(
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
        fields = (
            Feedback.text.field.name,
        )
        labels = {
            Feedback.text.field.name: 'Текст сообщения',
        }
