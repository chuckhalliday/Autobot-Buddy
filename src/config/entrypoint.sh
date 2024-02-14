#!/bin/bash

APP_PORT=${PORT:-8000}

cd /app/

# Run gunicorn
/opt/venv/bin/gunicorn autohome.wsgi:application --bind "0.0.0.0:${APP_PORT}"