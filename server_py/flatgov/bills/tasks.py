from celery import shared_task, current_app
from bills.models import BillUpdateJob


@shared_task(bind=True)
def update_bill_task(self):
    obj = BillUpdateJob.objects.create(job_id=self.request.id)
