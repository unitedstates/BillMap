from celery import shared_task, current_app
from uscongress.models import UscongressUpdateJob
from uscongress.handlers import govinfo, bills
from uscongress.helper import update_bills_meta
from common.billdata import saveBillsMeta
from common.process_bill_meta import makeAndSaveTitlesIndex
from common.relatedBills import makeAndSaveRelatedBills

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
        history.saved = processed.get('saved')
        history.skips = processed.get('skips')
        history.save(update_fields=['data_status', 'saved', 'skips'])
    except Exception as e:
        history.data_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['data_status'])
    return history.id


@shared_task(bind=True)
def bill_data_task(self, pk):
    bills_meta = dict()
    history = UscongressUpdateJob.objects.get(pk=pk)
    try:
        for bill_id in history.saved:
            bill_congress_type_number, related_dict = update_bills_meta(bill_id)
            bills_meta[bill_congress_type_number] = related_dict
        saveBillsMeta(bills_meta)
        history.bill_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['bill_status'])
    except Exception as e:
        history.bill_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['bill_status'])


@shared_task(bind=True)
def process_bill_meta_task(self, pk):
    history = UscongressUpdateJob.objects.get(pk=pk)
    try:
        makeAndSaveTitlesIndex()
        history.meta_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['meta_status'])
    except Exception as e:
        history.meta_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['meta_status'])


@shared_task(bind=True)
def related_bill_task(self, pk):
    history = UscongressUpdateJob.objects.get(pk=pk)
    try:
        makeAndSaveRelatedBills()
        history.related_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['related_status'])
    except Exception as e:
        history.related_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['related_status'])
