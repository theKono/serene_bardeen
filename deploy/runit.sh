#!/bin/bash

VENV_ACTIVATE=/home/ubuntu/.virtualenvs/serene_bardeen/bin/activate
GUNICORN=/usr/bin/gunicorn
ROOT=/home/ubuntu/serene_bardeen/current
PID=/var/run/gunicorn.pid
APP=main:application

if [ -f $PID ]; then rm $PID; fi

cd $ROOT
source $VENV_ACTIVATE
exec $GUNICORN -c $ROOT/deploy/gunicorn.config.py --pid=$PID $APP
