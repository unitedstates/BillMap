from django.core.management.base import BaseCommand
from common.statements import load_statements


class Command(BaseCommand):
    help = 'create bill data via billdata.py'

    def handle(self, *args, **options):
        load_statements()
