from django.core.management.base import BaseCommand
from common.biden_statements import load_statements
from common.tasks import scrape_statements_task

class Command(BaseCommand):
    help = 'loading Biden statements data from the scraped data.'

    def handle(self, *args, **options):
        load_statements()
