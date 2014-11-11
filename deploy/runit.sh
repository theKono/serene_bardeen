#!/bin/bash

GUNICORN=/usr/bin/gunicorn
ROOT=/home/ubuntu/serene_bardeen/current
PID=/var/run/gunicorn.pid
APP=serene_bardeen.main:application

if [ -f $PID ]; then rm $PID; fi

cd $ROOT
exec $GUNICORN -c $ROOT/deploy/gunicorn.config.py --pid=$PID $APP
