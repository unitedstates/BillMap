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

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--uncongress',
            action='store_true',
            help='Open source scraper - unitedstates/congress'
        )

    def handle(self, *args, **options):
        uncongress = options['uncongress']

        createIndex(delete=True)
        indexBills(uncongress=uncongress)
        refreshIndices()
        res = runQuery()
        billnumbers = getResultBillnumbers(res)
        print('Top matching bills: {0}'.format(', '.join(billnumbers)))
        innerResults = getInnerResults(res)
        print(innerResults)
