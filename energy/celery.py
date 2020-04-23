from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energy.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('energy')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'generate_csv': {
        'task': 'generate_csv',
        'schedule': crontab(minute='*/2') #crontab(minute=10, hour=9)
        },
    "write_to_db": {
        'task': 'write_to_db',
        'schedule': crontab(minute='*/8')    #crontab(minute=15, hour=9)
       }
}
