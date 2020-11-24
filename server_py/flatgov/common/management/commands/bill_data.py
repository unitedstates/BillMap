from django.core.management.base import BaseCommand
from common.billdata import updateBillsList, updateBillsMeta


class Command(BaseCommand):
    help = 'create bill data via billdata.py'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #                   "-a",
    #                   "--argument",
    #                   action='store',
    #                   dest='argument',
    #                   type=str,
    #                   help="sample argument")

    #     parser.add_argument(
    #                   "-v",
    #                   "--verbose",
    #                   dest='verbose',
    #                   help="increase output verbosity",
    #                   action="store_true")

    def handle(self, *args, **options):
        updateBillsList()
        updateBillsMeta()
