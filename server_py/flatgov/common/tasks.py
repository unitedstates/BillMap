from celery.task.schedules import crontab
import datetime
from django.utils import timezone
from celery.decorators import periodic_task
from .biden_statements import load_statements


@periodic_task(run_every=(crontab(minute=0, hour=0), name="scrape-biden-statements-once-a-day", ignore_result=True)
def scrape_statements_task():
        load_statements()
