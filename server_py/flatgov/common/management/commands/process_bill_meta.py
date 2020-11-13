from django.core.management.base import BaseCommand
from common.process_bill_meta import makeAndSaveTitlesIndex


class Command(BaseCommand):
    help = 'combines data from the results of the bill data, to get titles'

    def handle(self, *args, **options):
        makeAndSaveTitlesIndex()
