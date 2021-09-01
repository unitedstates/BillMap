import os
from typing import Optional
from server_py.flatgov.common.billdata import updateBillModelFields
from server_py.flatgov.common import constants
import subprocess
import shutil
from celery import shared_task, current_app
from uscongress.models import UscongressUpdateJob
from uscongress.handlers import govinfo, bills
from uscongress.helper import (
    create_es_index,
    es_index_bill,
    update_bills_meta,
    es_similarity_bill,
)
from common.billdata import saveBillsMeta, updateBillMetaToDbAll, saveBillsMetaToDb
from common.process_bill_meta import makeAndSaveTitlesIndex
from common.elastic_load import ( 
    refreshIndices,
    runQuery,
    getResultBillnumbers,
    getInnerResults,
)

from django.conf import settings
from common.constants import BILLMETA_GO_CMD, ESQUERY_GO_CMD, PATH_TO_BILLS_META_GO

GOVINFO_OPTIONS = {
    "collections": "BILLS",
    "bulkdata": "BILLSTATUS",
    "congress": str(constants.CURRENT_CONGRESS),
    "extract": "mods,xml,premis"
}

BILLS_OPTIONS = {}


@shared_task(bind=True)
def update_bill_task(self):
    history = UscongressUpdateJob.objects.create(job_id=self.request.id)
    try:
        # Downloads files from Govinfo
        # The govinfo.py file is copied from the uscongress repository
        govinfo.run(GOVINFO_OPTIONS)
        history.fdsys_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['fdsys_status'])
    except Exception as e:
        history.fdsys_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['fdsys_status'])
    try:
        # Creates data.json from the downloaded files 
        # The bills.py file is copied from the uscongress repository
        processed = bills.run(BILLS_OPTIONS)
        history.data_status = UscongressUpdateJob.SUCCESS
        if processed:
            history.saved = processed.get('saved')
            history.skips = processed.get('skips')
            history.save(update_fields=['data_status', 'saved', 'skips'])
    except Exception as e:
        history.data_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['data_status'])
    return history.id

def update_bills_meta_go():
    subprocess.run([BILLMETA_GO_CMD, '-p', settings.BASE_DIR])
    # Update only the current Congress metadata
    rootDir = os.path.join(constants.PATH_TO_CONGRESSDATA_DIR, str(constants.CURRENT_CONGRESS))
    updateBillMetaToDbAll(rootDir)
    #saveBillsMetaToDb()

def es_similarity_go(congress: Optional[str] = None):
    if congress:
        subprocess.run([ESQUERY_GO_CMD, '-p', settings.BASE_DIR, '-congress', congress, '-save'])
    else:
        subprocess.run([ESQUERY_GO_CMD, '-p', settings.BASE_DIR, '-save'])

    if congress:
        rootDir = os.path.join(constants.PATH_TO_CONGRESSDATA_DIR, congress)
    else:
        rootDir = constants.PATH_TO_CONGRESSDATA_DIR
    # Processes saved files for each bill and saves to database
    updateBillModelFields(rootDir)

@shared_task(bind=True)
def bill_data_task(self, pk):
    bills_meta = dict()
    history = UscongressUpdateJob.objects.get(pk=pk)
    try:
        if shutil.which(BILLMETA_GO_CMD) is not None:
            update_bills_meta_go()
        else:
            for bill_id in history.saved:
                bill_congress_type_number, related_dict, err = update_bills_meta(bill_id)
                if err:
                    continue
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
        # The Go version of update_bills_meta includes this task
        if shutil.which(BILLMETA_GO_CMD) is None:
            makeAndSaveTitlesIndex()
        #TODO: add a 'skipped' value for the UscongressUpdateJob model for the Go version
        history.meta_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['meta_status'])
    except Exception as e:
        history.meta_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['meta_status'])


@shared_task(bind=True)
def related_bill_task(self, pk):
    from common.relatedBills import makeAndSaveRelatedBills
    history = UscongressUpdateJob.objects.get(pk=pk)
    try:
        # The Go version of update_bills_meta includes this task
        if shutil.which(BILLMETA_GO_CMD) is None:
            makeAndSaveRelatedBills()
        history.related_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['related_status'])
    except Exception as e:
        history.related_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['related_status'])


@shared_task(bind=True)
def elastic_load_task(self, pk):
    history = UscongressUpdateJob.objects.get(pk=pk)
    try:
        created = create_es_index()
        for bill_id in history.saved:
            res = es_index_bill(bill_id)
        refreshIndices()
        # These functions get all bills indexed in Elasticsearch 
        # TODO: save these (or the total number) as is done in update_bill_task
        # res = runQuery()
        # billnumbers = getResultBillnumbers(res)
        # innerResults = getInnerResults(res)
        history.elastic_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['elastic_status'])
    except Exception as e:
        history.elastic_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['elastic_status'])


@shared_task(bind=True)
def bill_similarity_task(self, pk):
    history = UscongressUpdateJob.objects.get(pk=pk)
    try:
        if shutil.which(BILLMETA_GO_CMD) is None:
            # ESQUERY_GO_CMD is available
            # This processes all bills in Elasticsearch for the current Congress
            # Saves the results to a number of files
            # Then saves those files to the database
            es_similarity_go(str(constants.CURRENT_CONGRESS))
        else:
            for bill_id in history.saved:
                res = es_similarity_bill(bill_id)
        history.similarity_status = UscongressUpdateJob.SUCCESS
        history.save(update_fields=['similarity_status'])
    except Exception as e:
        history.similarity_status = UscongressUpdateJob.FAILED
        history.save(update_fields=['similarity_status'])
