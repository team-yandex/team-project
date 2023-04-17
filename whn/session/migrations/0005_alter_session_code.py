# Generated by Django 3.2.18 on 2023-04-16 08:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_alter_session_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, help_text='код сессии', verbose_name='код'),
        ),
    ]
