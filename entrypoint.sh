#!/bin/bash -x

python manage.py makemigrations --no-input
python manage.py migrate --noinput 
exec gunicorn myshows.wsgi:application --worker-class gevent -b 0.0.0.0:8000 --reload
