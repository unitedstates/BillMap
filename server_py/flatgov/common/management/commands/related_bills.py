import os

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from common.relatedBills import makeAndSaveRelatedBills


class Command(BaseCommand):
    help = '''processes the data above to add related bills and sponsor 
            data to each file in `congress/datsa/relatedbills'''

    def handle(self, *args, **options):
        if os.getenv('DJANGO_SETTINGS_MODULE') and os.getenv('SECRET_KEY'):
            makeAndSaveRelatedBills()
        else:
            msg = 'DJANGO_SETTINGS_MODULE & SECRET_KEY missing from env vars.'
            ValidationError(msg)
