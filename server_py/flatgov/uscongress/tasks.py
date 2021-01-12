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
    history = UscongressUpdateJob.objects.create(job_id=self.request.id)
    try:
        govinfo.run(GOVINFO_OPTIONS)
        history.fdsys_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['fdsys_status'])
    except Exception as e:
        history.fdsys_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['fdsys_status'])
    try:
        processed = bills.run(BILLS_OPTIONS)
        history.data_status = UscongressUpdateJob.SUCCESS
        history.content = processed
        history.save(update_fields=['data_status', 'content'])
    except Exception as e:
        history.data_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['data_status'])
    return history.id


@shared_task(bind=True)
def bill_data_task(self, pk):
    history = UscongressUpdateJob.objects.get(pk=pk)

