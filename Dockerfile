FROM python:3.11-slim

WORKDIR /app

COPY requirements/prod.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

ENV DJANGO_ALLOWED_HOSTS=egame-lyceum.ru,127.0.0.1:8000,46.17.102.34,
ENV DJANGO_DEBUG=False

RUN python egame/manage.py migrate --noinput

RUN python egame/manage.py loaddata egame/fixtures/tasks.json
RUN python egame/manage.py loaddata egame/fixtures/achievements.json
RUN python egame/manage.py loaddata egame/fixtures/users.json
RUN python egame/manage.py loaddata egame/fixtures/preparation.json

EXPOSE 8000

CMD ["python", "egame/manage.py", "runserver", "0.0.0.0:8000"]