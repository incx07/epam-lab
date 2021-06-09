#!/bin/bash -x

python myshows/manage.py makemigrations --no-input
python myshows/manage.py migrate --noinput 
python myshows/manage.py runserver 0.0.0.0:8000
