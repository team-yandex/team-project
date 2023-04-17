# Generated by Django 3.2.18 on 2023-04-11 13:31

import django.core.validators
from django.db import migrations, models


def create_climax_videos(apps, schema_editor):
    import game.models
    
    Question = apps.get_model('game', 'Question')
    for question in Question.objects.all():
        game.models.Question.save(question)


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='climax_video',
            field=models.FileField(auto_created=True, blank=True, null=True, upload_to='video', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], verbose_name='видео с кульминацией'),
        ),
        migrations.RunPython(create_climax_videos, reverse_code=migrations.RunPython.noop),
    ]
