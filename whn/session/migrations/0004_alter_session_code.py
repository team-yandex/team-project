# Generated by Django 3.2.18 on 2023-04-16 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_alter_session_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='code',
            field=models.CharField(default='7a4af02b052f41bd8816dfe0acab8ba2', help_text='код сессии', max_length=200, verbose_name='код'),
        ),
    ]