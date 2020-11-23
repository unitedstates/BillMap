from django.core.management.base import BaseCommand
from common.elastic_load import (
    createIndex, 
    indexBills,
    refreshIndices,
    runQuery,
    getResultBillnumbers,
    getInnerResults
)

class Command(BaseCommand):
    help = 'create bill data via billdata.py'

    def handle(self, *args, **options):
        createIndex(delete=True)
        indexBills()
        refreshIndices()
        res = runQuery()
        billnumbers = getResultBillnumbers(res)
        print('Top matching bills: {0}'.format(', '.join(billnumbers)))
        innerResults = getInnerResults(res)
        print(innerResults)
