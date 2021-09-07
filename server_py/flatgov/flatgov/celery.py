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
    'update_bills_daily': {
        # Triggers bill download
        # When this completes and SUCCESS= True,
        # The rest of the bill similarity tasks are triggered in uscongress/models.py
        'task': 'uscongress.tasks.update_bill_task',
        'schedule': crontab(minute=1, hour=1),
        'options': {'queue': 'bill'}
    },
    'sap_biden_scraper_daily': {
        # this task is independent of other tasks
        # It takes less than 1 minute
        'task': 'bills.tasks.sap_biden_task',
        'schedule': crontab(minute=0, hour=3),
        'options': {'queue': 'bill'}
    },
    'committee_report_scraper_daily': {
        # this task depends on updates from the update_bills task
        # It takes less than 5 minutes
        'task': 'bills.tasks.committee_report_scrapy_task',
        'schedule': crontab(minute=10, hour=3),
        'options': {'queue': 'bill'}
    },
    'update_cbo_scores_daily': {
        # this task depends on updates from the update_bills task
        # it runs on only the directory of the current congress
        # and should take less than 20 minutes 
        'task': 'bills.tasks.cbo_task',
        'schedule': crontab(minute=30, hour=3),
        'options': {'queue': 'bill'}
    },
    'update_cosponsor_daily': { 
        # the update_cosponsor task deletes the cosponsor table and recreates it
        # it takes about 1 hour to run
        # this is independent of other tasks, since it gets data directly 
        # from the YAML file in the unitedstates Github repo
        'task': 'bills.tasks.update_cosponsor_comm_task',
        'schedule': crontab(minute=20, hour=4),
        'options': {'queue': 'bill'}
    },
    'crs_scraper_daily': {
        # this task depends on updates from the update_bills task 
        # to link reports to bills
        'task': 'bills.tasks.crs_task',
        'schedule': crontab(minute=0, hour=5),
        'options': {'queue': 'bill'}
    },
}

app.conf.timezone = 'UTC'