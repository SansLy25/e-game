FROM python:3.11

WORKDIR /app

COPY requirements/dev.txt requirements/dev.txt

RUN pip install -r requirements/dev.txt

COPY Makefile /app/Makefile

COPY . .