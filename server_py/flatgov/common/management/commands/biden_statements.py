from json import load
from django.core.management.base import BaseCommand
from common.biden_statements import load_biden_statements

class Command(BaseCommand):
    help = 'loading Biden statements data from the scraped data.'

    def handle(self, *args, **options):
        load_biden_statements()
