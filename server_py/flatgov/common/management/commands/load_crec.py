from django.core.management.base import BaseCommand

from bills.models import CommitteeDocument
from common.crec_data import crec_loader


class Command(BaseCommand):
    help = 'loading committee documents from the scraped data.'

    def handle(self, *args, **options):
        CommitteeDocument.objects.all().delete()
        crec_loader()
