#!/usr/bin/env bash
set -o errexit

pip install -r prodify/requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
