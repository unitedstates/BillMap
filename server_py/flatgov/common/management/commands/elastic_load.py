from django.core.management.base import BaseCommand
from common.constants import BILL_FULL_MAPPING 
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

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--uscongress',
            action='store_true',
            help='Open source scraper - unitedstates/congress'
        )
        parser.add_argument(
            '-i',
            '--index',
            action='store',
            help='Index type - sections or full_bill'
        )

    def handle(self, *args, **options):
        uscongress = options['uscongress']

        if not options['index'] or options['index'] == 'sections':
            createIndex(delete=True)
            indexBills(uscongress=uscongress)
        else:
            if options['index'] == 'bill_full':
                print('Using option "bill_full"')
                createIndex(index='bill_full', body=BILL_FULL_MAPPING, delete=True,)
            indexBills(uscongress=uscongress, index_types=['bill_full'])
        refreshIndices()