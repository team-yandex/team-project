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
Перейти в папку requirements: 
```bash
cd requirements
```
- Основной - для запуска сервера: ```pip install -r requirements-prod.txt```
- Дополнительный - для тестов: ```pip install -r requirements-test.txt```
- Дополнительный - для разработки: ```pip install -r requirements-dev.txt``` 

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

## ER диаграмма моделей
https://app.quickdatabasediagrams.com/#/d/YbqEiX  
(вставить картинку)

## For developers

[Django](https://docs.djangoproject.com/en/3.2/) documentation
