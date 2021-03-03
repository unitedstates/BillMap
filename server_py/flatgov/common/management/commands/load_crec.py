from django.core.management.base import BaseCommand
from common.crec_data import crec_loader
from bills.models import CommitteeDocument



class Command(BaseCommand):
    help = 'create cbo data.'

    def handle(self, *args, **options):
        CommitteeDocument.objects.all().delete()

        crec_loader()
