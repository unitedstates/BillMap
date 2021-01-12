from celery import shared_task, current_app
from uscongress.models import UscongressUpdateJob


@shared_task(bind=True)
def update_bill_task(self):
    obj = UscongressUpdateJob.objects.create(job_id=self.request.id)
