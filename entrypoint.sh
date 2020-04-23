#!/bin/sh

# wait for PSQL server to start
sleep 5

#python manage.py migrate
python upload_data.py
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
#su -m myuser -c "python upload_data.py"
#su -m myuser -c "python manage.py migrate"
#su -m myuser -c "python manage.py runserver 0.0.0.0:8000"