#!/bin/bash

set -e

# Trap CTRL+C (SIGINT)
trap 'echo -e "\nExiting"; kill 0; wait; exit' INT

uv run python manage.py collectstatic --noinput
uv run python manage.py migrate
uv run gunicorn payment.wsgi &

uv run celery -A payment worker -l info &

uv run celery -A payment beat -l info &

wait
