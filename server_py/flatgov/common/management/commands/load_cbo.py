from django.core.management.base import BaseCommand
from common.cbo import cbo
from bills.models import Transaction

class Command(BaseCommand):
    help = 'create cbo data.'

    def handle(self, *args, **options):
        Transaction.objects.all().delete()
        cbo()
