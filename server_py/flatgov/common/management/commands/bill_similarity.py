import os

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from common.relatedBills import makeAndSaveRelatedBills
from common.bill_similarity import indexBills


class Command(BaseCommand):
    help = '''processes the data above to add similarity to bills'''

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--uncongress',
            action='store_true',
            help='Open source scraper - unitedstates/congress'
        )

    def handle(self, *args, **options):
        if os.getenv('DJANGO_SETTINGS_MODULE') and os.getenv('SECRET_KEY'):
            uncongress = options['uncongress']
            indexBills(uncongress=uncongress)
        else:
            msg = 'DJANGO_SETTINGS_MODULE & SECRET_KEY missing from env vars.'
            ValidationError(msg)