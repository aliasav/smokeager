#!/bin/bash

NAME="smokeager"                                  # Name of the application
DJANGODIR=/home/aliasav/workspace/smokeager # Django project directory
USER=aliasav                                      # the user to run as
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=smokeager.settings             # which settings file should Django use
LOGFILE=/var/log/celerybeat.log

echo "Starting $NAME celerybeat"

# Activate the virtual environment
cd $DJANGODIR
source /home/aliasav/virtualenvs/smokeager/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec python manage.py celery beat --loglevel=INFO --logfile=$LOGFILE
