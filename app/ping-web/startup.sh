#!/bin/bash

python manage.py migrate --noinput
python manage.py createsuperuser --noinput
python manage.py collectstatic
