#!/bin/sh

echo "Running migrations..."
python manage.py makemigrations 
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn payment.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --log-level info
