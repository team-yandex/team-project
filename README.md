[![build](https://github.com/team-yandex/team-project/actions/workflows/build.yml/badge.svg)](https://github.com/team-yandex/team-project/actions/workflows/build.yml)
![](https://img.shields.io/badge/django-3.2.18-green)
![](https://img.shields.io/badge/python-3.9-brightgreen)
# What happened next?

Угадайте по видео, что будет дальше.
Проект доступен по адресу: http://whn.hopto.org/  

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

- Python 3.7
- Django 3.2
- PostgreSQL
- Nginx
- Gunicorn
- Docker, Docker Hub
- GitHubActions(CI/CD)
- JS & jQuery

## Quick start

### Clone the repository:
```bash
git clone https://github.com/team-yandex/team-project.git
```

### Create a virtual environment:

Windows:
```bash
python -m venv venv
```
Mac, Linux:
```bash
python3 -m venv venv
```

### Activate the virtual environment:

Windows:
```bash
.\venv\Scripts\activate.bat
```
Mac, Linux:
```bash
source venv/bin/activate
```

### Install dependencies:
Go to requirements: 
```bash
cd requirements
```
- master - to run server: ```pip install -r requirements-prod.txt```
- additional - for test: ```pip install -r requirements-test.txt```
- additional - for development: ```pip install -r requirements-dev.txt``` 

Also you need Redis on your machine to run project:
[Install Redis](https://redis.io/docs/getting-started/installation/)

For example, in Arch Linux:
```bash
sudo pacman -S redis
sudo systemctl enable --now redis.service
```

### Configure

You should use dotenv to configure settings. Example:
```
SECRET_KEY = VERYSECRETKEY
DEBUG = false
ALLOWED_HOSTS = 192.168.0.21,192.168.0.1
```

You can use example dotenv:

```bash
cp example.env .env
```

You have to migrate your database:
```bash
python whn/manage.py migrate
```

To add data and videos go to [Initdata](####initdata) section


### Launch:

#### Django server:
```bash
cd whn
```

Windows:
```bash
python manage.py runserver
```
Mac, Linux:
```bash
python3 manage.py runserver
```

## Запуск проекта в Docker контейнере

- Установите Docker.
- (Далее) Установите драйвер psycopg2-binary внутри контейнера (Для Postgres)

Параметры запуска описаны в файлах docker-compose.yml и nginx.conf которые находятся в директории infra/

- Запустите docker compose:

```bash
docker-compose up -d --build
```  

  > После сборки появляются 3 контейнера:
  >
  > 1. контейнер базы данных db
  > 2. контейнер приложения backend
  > 3. контейнер web-сервера nginx
  >

```bash
docker-compose exec web python manage.py migrate
```

- Создайте суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

- Запустите процесс сбора статики:

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

- Не забудьте запустить сервер с параметром --settings=whn.settings_prod

## ER diagram

![erd](https://user-images.githubusercontent.com/88326901/233119504-d27abdde-dbeb-4ad8-a94d-32a1231b69ae.svg)

## For developers

[Django](https://docs.djangoproject.com/en/3.2/) documentation

### Custom commands

#### `initdata`

If you want to populate your fresh db with fixtures and superuser creditinals you can use

Windows:
```bash
cd whn
python manage.py initdata
```
Mac, Linux:
```bash
cd whn
python3 manage.py initdata
```

This command will check migrations and if there are pending ones you can apply them in place.

After that command will create superuser with creditinals defined in enviroment variables like

```
DJANGO_SUPERUSER_USERNAME = admin
DJANGO_SUPERUSER_EMAIL = admin@email.com
DJANGO_SUPERUSER_PASSWORD = superuserpassword
```

You could input all your creditinal from stdin if you haven't specified settings in enviroment variables. 

### ER diagram generation

You should define enviroment variable for app containing models:

```
GRAPH_APPS=core,feedback,game,info,users
```

After you sould run:

```
python manage.py graph_models -o <filename>.<image extension>
```

For example: `python manage.py graph_models -o erd.svg`

For more info look at [django extension documentation](https://django-extensions.readthedocs.io/en/latest/graph_models.html#graph-models)
