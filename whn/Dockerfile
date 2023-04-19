FROM python:3.8-slim

WORKDIR /app

COPY requirements-prod.txt .

RUN pip3 install -r requirements-prod.txt --no-cache-dir

COPY . .

CMD ['gunicorn', 'whn.wsgi:application', '--bind', '0:8000' ]
