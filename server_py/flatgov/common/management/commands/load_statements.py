from django.core.management.base import BaseCommand
from common.statements import load_statements


class Command(BaseCommand):
    help = 'loading statements data from the scraped data.'

    def handle(self, *args, **options):
        load_statements()
