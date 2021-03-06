#!/bin/bash
echo STARTINGD RUN.SH FOR STARTING DJANGO SERVER PORT IS $PORT
#
#echo ENVIRONMENT VAIRABLES IN RUN.SH
#printenv
#Change this values for django superuser
if [ -z "$VCAP_APP_PORT" ];
  then SERVER_PORT=5000;
  else SERVER_PORT="$VCAP_APP_PORT";
fi
echo [$0] port is------------------- $SERVER_PORT
# python manage.py makemigrations
# python manage.py migrate
echo [$0] Starting Django Server...
rm db.sqlite
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data_dump.json
python email_trigger.py &
python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload