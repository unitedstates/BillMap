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
            '--uscongress',
            action='store_true',
            help='Open source scraper - unitedstates/congress'
        )

    def handle(self, *args, **options):
        uscongress = options['uscongress']

        createIndex(delete=True)
        indexBills(uscongress=uscongress)
        refreshIndices()