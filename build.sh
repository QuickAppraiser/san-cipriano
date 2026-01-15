#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Compile translation messages
python manage.py compilemessages --ignore=.venv

python manage.py collectstatic --no-input
python manage.py migrate
