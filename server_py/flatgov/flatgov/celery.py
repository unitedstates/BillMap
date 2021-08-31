import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flatgov.dev')

app = Celery('flatgov')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.redbeat_redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.conf.broker_pool_limit = 1
app.conf.broker_heartbeat = None
app.conf.broker_connection_timeout = 30
app.conf.worker_prefetch_multiplier = 1

app.conf.beat_schedule = {
    'download_sources': {
        'task': 'events.tasks.download_sources',
        'schedule': crontab(minute=0, hour=19)
    },
    'process_sources': {
        'task': 'events.tasks.process_sources',
        'schedule': crontab(minute=5, hour=19)
    },
    'update_cbo_scores': {
        'task': 'bills.tasks.cbo_task',
        'schedule': crontab(minute=0, hour=1),
        'options': {'queue': 'bill'}
    },
    'sap_scraper_daily': {
        'task': 'bills.tasks.sap_scrapy_task',
        'schedule': crontab(minute=0, hour=2),
        'options': {'queue': 'bill'}
    }, # Biden statements would go next, but there is currently a bug
    'update_cosponsor': { 
        # the update_cosponsor task deletes the cosponsor table and recreates it
        # it takes about 1 hour to run
        'task': 'bills.tasks.update_cosponsor_comm_task',
        'schedule': crontab(minute=20, hour=2),
        'options': {'queue': 'bill'}
    },
    'crs_scraper_daily': {
        'task': 'bills.tasks.crs_task',
        'schedule': crontab(minute=0, hour=1),
        'options': {'queue': 'bill'}
    },
}

app.conf.timezone = 'UTC'
