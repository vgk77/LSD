#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py migrate
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
gunicorn -w 3 -b :5000 config.wsgi:application
