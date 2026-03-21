#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python crear_usuarios.py
gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --worker-class sync SGIEVpy.wsgi:application
