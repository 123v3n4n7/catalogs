#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
exec gunicorn catalogs.wsgi:application -b 0.0.0.0:8000 --reload
#python manage.py runserver 0.0.0.0:8000