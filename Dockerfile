FROM python:3.12-slim

WORKDIR /app

COPY requirements/prod.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

EXPOSE 8000

CMD bash -c "cd egame && python manage.py migrate --noinput && \
             python manage.py loaddata fixtures/tasks.json && \
             python manage.py loaddata fixtures/achievements && \
             python manage.py loaddata fixtures/users.json && \
             python manage.py loaddata fixtures/preparation.json && \
             gunicorn --bind 0.0.0.0:8000 egame.wsgi:application"