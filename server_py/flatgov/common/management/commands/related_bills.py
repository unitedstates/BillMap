from django.core.management.base import BaseCommand
from common.relatedBills import makeAndSaveRelatedBills


class Command(BaseCommand):
    help = '''processes the data above to add related bills and sponsor 
            data to each file in `congress/datsa/relatedbills'''

    def handle(self, *args, **options):
        makeAndSaveRelatedBills()
