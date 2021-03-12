from celery.task.schedules import crontab
import datetime
from django.utils import timezone
from celery.decorators import periodic_task
from .biden_statements import load_statements


@periodic_task(run_every=(crontab(0, 0, day_of_month='1')), name="scrape-statements-once-a-month", ignore_result=True)
def scrape_statements_task():
    load_statements()
