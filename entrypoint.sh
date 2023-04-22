#!/usr/bin/env bash

python manage.py migrate
python manage.py collectstatic --noinput
daphne whn.asgi:application -b 0.0.0.0 -p 8000
