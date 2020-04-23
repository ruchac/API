# EnergyData
This project aims extracting the Node Consumption data using node id and cron job. Saving the Extracted data into .csv & further the data pushed into PostgresSQL.
The API is created to check & extract the data by node id, month and year.
The Data can be visible in API by uploding the historical data or using current data extracted using cron job. 
<br /> In cron file need to set 2 cron job in time interval:
<br /> 1st cron job  will extract the new data into .csv & save it to the Data folder which will create at first run. 
<br /> 2nd Cron job The extracted .csv data will get pushed into PostgresSQL.

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
│   │   models.py               Script for joining Metadata & YearlyResult Data
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
## Database Schema
![image](https://user-images.githubusercontent.com/48212234/79697304-ddad5780-8279-11ea-892e-c5ea1168d10b.png)
<br /> The Metadata Table contains the information about the Node Id which is uploaded into PostgresSQL after running Docker command.
The .csv of the metadata is saved in hostorical data folder.
## Instruction
1. Add the Secret API key into the file task.py which is in downloadcsv folder.
2. To install Django Manually:
<br /> Create a virtual environment for the project:
```
$ mkvirtualenv energy
```
* Install Django:
```
$ pip install django==2.2.7
```
* Create django project and initial setup:
```
$ django-admin startproject <name_project>
```
3. To Use historical data:
<br /> Save the YearlyResult_().csv file into historical data & change the file path in upload_data.py file. 
```
        cur = conn.cursor()
        table_name = 'downloadcsv_metadata' #'downloadcsv_yearlyresult'
        with open(file_path, "r") as f:
            next(f)
            cur.copy_from(f, table_name, sep=',')
        conn.commit()
    except Exception as e:
        print("Error: {}".format(str(e)))
        sys.exit(1)

file_path = os.path.join("historical_data/Metadata.csv") #'YearlyResult.csv' # Change the file path.
pg_load_table(file_path)
```
Change the file path in _table_name = 'downloadcsv_yearlyresult'_** & _file_path = os.path.join("historical_data/_YearlyResult_().csv")_**

4. **For Cron Job Setting:**
<br /> Change the celery.py which is located in energy folder in order to set cron job for generate CSV & write to db.
<br /> For more celery refer to [celery](https://docs.celeryproject.org/en/2.0-archived/getting-started/periodic-tasks.html)
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
5. To run the app, docker and docker-compose must be installed on your system. For installation 
instructions refer to the [Docker](https://docs.docker.com/compose/install/).
``` 
docker-compose up --build
```
* **To Create Django Superuser:**
6. To access the registered user, the superuser can created using Django.
```
python manage.py createsuperuser

```

## To check the API:
1. To register a new user:
* http://127.0.0.1:8001/auth/registration
2. To login user:
* http://localhost:8001/auth/login/
<br /> A Superuser can check the registered users & give access by checking localhost:8000 into the web brower. 
3. To check API in action:
* http://localhost:8001/nodeconssunptions/{node_id}/{month}/{year}/
4. For API Documentation:
* http://localhost:8001/api_documentation/

