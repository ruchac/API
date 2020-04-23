# EnergyData
This project aims extracting the Node Consumption data using node id using cron job. Saving the Extracted data into .CSV & further the data pushed into PostgresSQL.
The API is created to check & extract the data by node id, month and year.

## Prerequisites ##
* Docker
* Docker compose

## File Structure ##
``` bash
│   celerybeat-schedule.dat
│   docker-compose.yml
│   Dockerfile			    dockerfile
│   entrypoint.sh
│   manage.py
│   requirements.txt
│   upload_data.py		    Script for uploading historical data
├───.idea
├───downloadcsv
│   │   admin.py
│   │   ae_api_client.py
│   │   ae_api_client.pyc
│   │   apps.py
│   │   models.py           Script for joining Metadata & YearlyResult Data
│   │   tasks.py			Main script for extraction of data  
│   │   tests.py
│   │   views.py
│   │   __init__.py
│   ├───management
│   │   ├───commands
│   │   │   │   dailyrating.py
│   ├───migrations
├───energy
│   │   asgi.py
│   │   celery.py			Job Schedular script
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
├───historical_data		    folder for historical data
│       Metadata.csv
└───UCDenergy
    │   admin.py
    │   apps.py
    │   models.py
    │   permission.py
    │   serializers.py
    │   tests.py
    │   views.py
    │   __init__.py
```

## Instruction
* **For Cron Job Setting:**
Change the celery.py in order to set cron job for generate CSV & write to db For more celery refer to [celery](https://docs.celeryproject.org/en/2.0-archived/getting-started/periodic-tasks.html)
    * Crontab Syntax: (minute=*, hour=*, Second=*)
    * If need to set Crontab for just minute : (minute='*/2')

```
app.conf.beat_schedule = {
.
    'generate_csv': {
        'task': 'generate_csv',
        'schedule': crontab(minute=10, hour=9) # 9:10 am
        },
    "write_to_db": {
        'task': 'write_to_db',
        'schedule': crontab(minute=15, hour=9) #9:15 am
       }
```

* **To build & run container:**
To run the app, docker and docker-compose must be installed on your system. For installation instructions refer to the [Docker](https://docs.docker.com/compose/install/).
``` 
docker-compose up --build
```
* **To Create Django Superuser:**
To access the registered user, the superuser can created using Django
```
python manage.py createsuperuser

```

## To check the API:
To register a new user:
* http://127.0.0.1:8001/auth/registration
To login user:
* http://localhost:8001/auth/login/
To check API in action:
* http://localhost:8001/nodeconssunptions/{node_id}/{month}/{year}/
For API Documentation:
* http://localhost:8001/api_documentation/

## To install Django:
1. Create a virtual environment for the project:
```
mkvirtualenv energy
```
2. Install Django:
```
pip install django==2.2.7
```
3. Create django project and initial setup:
```
django-admin startproject energy
```


