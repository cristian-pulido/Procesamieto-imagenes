#!/bin/bash

source /home/colciencias/Envs/ip/bin/activate

#exec gunicorn SanJose.wsgi --bind 0.0.0.0:8000 
#cd /home/colciencias/IP/Procesamieto-imagenes/ip
SCRIPT=`realpath $0`
cd `dirname $SCRIPT`
celery worker -A ip --without-mingle --loglevel=INFO --concurrency=3 -n pro@%h
#--broker=amqp://col2:col2@localhost:5672/image
