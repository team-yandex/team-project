[![build](https://github.com/team-yandex/team-project/actions/workflows/build.yml/badge.svg)](https://github.com/team-yandex/team-project/actions/workflows/build.yml)

# What happened next?

Угадайте по видео, что будет дальше.

## Quick start

### Clone the repository:
```bash
git clone https://github.com/TheMerret/intensive-django.git
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
cd venv/Scripts/
```
```bash
.\activate
```
Mac, Linux:
```bash
source venv/bin/activate
```

### Install dependencies:

Windows:
```bash
pip install -r requirements.txt
```
Mac, Linux:
```bash
pip3 install -r requirements.txt
```

For development:

```
requirements-dev.txt
```

For testing:

```
requirements-test.txt
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
## For developers

[Django](https://docs.djangoproject.com/en/3.2/) documentation
