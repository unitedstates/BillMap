from django.core.management.base import BaseCommand
from common.crec_data import crec_loader
from bills.models import CommitteeDocument



class Command(BaseCommand):
    help = 'loading committee documents from the scraped data.'

    def handle(self, *args, **options):
        CommitteeDocument.objects.all().delete()

        crec_loader()
