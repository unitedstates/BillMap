from django.core.management.base import BaseCommand
from common.biden_statements import load_statements

class Command(BaseCommand):
    help = 'loading Biden statements data from the scraped data.'

    def handle(self, *args, **options):
        load_statements()
