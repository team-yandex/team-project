import django.forms


import game.models


class QuestionForm(django.forms.Form):
    choices = django.forms.ModelChoiceField(
        queryset=game.models.Choice.objects.none(),
        widget=django.forms.RadioSelect,
        required=True,
        label='Что будет дальше?',
    )

    def __init__(self, *args, instance, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'].queryset = instance.choices.all()
