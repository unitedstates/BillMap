import os
import logging

from django.core.management.base import BaseCommand
from uscongress.handlers import govinfo, bills
from common import constants


GOVINFO_OPTIONS = {
    'collections': 'BILLS',
    'bulkdata': 'BILLSTATUS',
    'extract': 'mods,xml,premis',
}

CONGRESS = str(constants.CURRENT_CONGRESS)

BILLS_OPTIONS = {}


class Command(BaseCommand):
    help = '''update bill text and metadata by using uscongress open source scraper'''

    def handle(self, *args, **options):
        for congress in CONGRESS:
            GOVINFO_OPTIONS['congress'] = congress
            govinfo.run(GOVINFO_OPTIONS)
            processed = bills.run(BILLS_OPTIONS)
