from django.core.management.base import BaseCommand
from common.cbo import cbo
from bills.models import CboReport

class Command(BaseCommand):
    help = 'create cbo data.'

    def handle(self, *args, **options):
        CboReport.objects.all().delete()
        cbo()
