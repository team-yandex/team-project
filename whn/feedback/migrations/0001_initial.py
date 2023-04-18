# Generated by Django 3.2.18 on 2023-04-15 12:14

from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Максимальная длина 200 символов', max_length=200, verbose_name='текст')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Когда был написан отзыв', verbose_name='дата создания')),
                ('status', models.CharField(choices=[('get', 'Получено'), ('saw', 'В обработке'), ('ans', 'Ответ дан')], default='get', help_text='Что сейчас происходит с отзывом', max_length=3, verbose_name='статус обработки')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
        migrations.CreateModel(
            name='FeedbackFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to=feedback.models.FeedbackFile.get_path, verbose_name='файл')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='feedback.feedback')),
            ],
            options={
                'verbose_name': 'файл отзыва',
                'verbose_name_plural': 'файлы отзывов',
                'default_related_name': 'files',
            },
        ),
        migrations.CreateModel(
            name='FeedbackAuther',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимальная длина 64 символа', max_length=64, verbose_name='имя')),
                ('email', models.EmailField(help_text='Максимум 254 символа', max_length=254, verbose_name='почта')),
                ('feedback', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auther', to='feedback.feedback')),
            ],
            options={
                'verbose_name': 'персональные данные автора отзыва',
                'verbose_name_plural': 'персональные данные авторов отзывов',
                'default_related_name': 'auther',
            },
        ),
    ]
