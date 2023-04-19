[![build](https://github.com/team-yandex/team-project/actions/workflows/build.yml/badge.svg)](https://github.com/team-yandex/team-project/actions/workflows/build.yml)
![](https://img.shields.io/badge/django-3.2.18-green)
![](https://img.shields.io/badge/python-3.9-brightgreen)
# What happened next?

Угадайте по видео, что будет дальше.

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

### Launch:

#### Django server:

Windows:
```bash
python manage.py runserver
```
Mac, Linux:
```bash
python3 manage.py runserver
```

## ER diagram

![erd](https://user-images.githubusercontent.com/88326901/233119504-d27abdde-dbeb-4ad8-a94d-32a1231b69ae.svg)

## For developers

[Django](https://docs.djangoproject.com/en/3.2/) documentation

### Custom commands

#### `initdata`

If you want to populate your fresh db with fixtures and superuser creditinals you can use

Windows:
```bash
python manage.py initdata
```
Mac, Linux:
```bash
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
