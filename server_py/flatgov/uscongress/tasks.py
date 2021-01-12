from celery import shared_task, current_app
from uscongress.models import UscongressUpdateJob
from uscongress.handlers import govinfo, bills

GOVINFO_OPTIONS = {
    'bulkdata': 'BILLSTATUS',
    'congress': '117'
}

BILLS_OPTIONS = {}


@shared_task(bind=True)
def update_bill_task(self):
    obj = UscongressUpdateJob.objects.create(job_id=self.request.id)
    govinfo.run(GOVINFO_OPTIONS)
    bills.run(BILLS_OPTIONS)
