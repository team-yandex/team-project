# Generated by Django 3.2.18 on 2023-04-15 09:31
from os import environ

from django.conf import settings
from django.core.management import call_command
from django.db import migrations, models
import django.db.models.deletion


def create_superuser():
    superuser_env_variables = [
        "DJANGO_SUPERUSER_USERNAME",
        "DJANGO_SUPERUSER_PASSWORD",
    ]
    is_superuser_prompt_interactive = not all(
        environ.get(var) for var in superuser_env_variables
    )
    call_command(
        "createsuperuser",
        interactive=is_superuser_prompt_interactive,
    )


def create_authors(apps, schema_editor):
    Question = apps.get_model('game', 'Question')
    User = apps.get_model('users', 'User')
    admin = User.objects.filter(is_superuser=True).first()
    if admin is None:
        create_superuser()
    for question in Question.objects.all():
        question.author = admin
        question.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0005_default_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(blank=True, help_text='укажите автора вопроса', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.RunPython(create_authors, reverse_code=migrations.RunPython.noop),
    ]
