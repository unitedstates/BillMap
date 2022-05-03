from django.core.management.base import BaseCommand

from bills.models import CboReport
from common.cbo import cbo


class Command(BaseCommand):
    help = 'loading cbo data.'

    def handle(self, *args, **options):
        CboReport.objects.all().delete()
        cbo()
