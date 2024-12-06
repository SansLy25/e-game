FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements/dev.txt /app/requirements/dev.txt

RUN pip install --no-cache-dir -r requirements/dev.txt

COPY Makefile /app/Makefile

COPY . /app/