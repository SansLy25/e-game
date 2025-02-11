FROM python:3.12-slim

WORKDIR /app

COPY requirements/prod.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

ENV DJANGO_ALLOWED_HOSTS=egame-lyceum.ru
ENV DJANGO_DEBUG=False

EXPOSE 8000

CMD bash -c "python egame/manage.py migrate --noinput && \
             python egame/manage.py loaddata egame/fixtures/tasks.json && \
             python egame/manage.py loaddata egame/fixtures/users.json && \
             python egame/manage.py loaddata egame/fixtures/preparation.json && \
             python egame/manage.py runserver 0.0.0.0:8000"