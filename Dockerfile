FROM python:3.9-slim

WORKDIR /app

COPY ./requirements/requirements-prod.txt .

RUN pip3 install -r requirements-prod.txt --no-cache-dir

COPY ./whn .

COPY ./entrypoint.sh .
