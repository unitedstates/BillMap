import os
import logging

from django.core.management.base import BaseCommand
from uscongress.handlers import govinfo, bills

GOVINFO_OPTIONS = {
    'collections': 'BILLS',
    'bulkdata': 'BILLSTATUS',
    'extract': 'mods,xml,premis',
}

CONGRESS = ['113', '114', '115', '116']

BILLS_OPTIONS = {}


class Command(BaseCommand):
    help = '''update bill text and metadata by using uscongress open source scraper'''

    def handle(self, *args, **options):
        for congress in CONGRESS:
            GOVINFO_OPTIONS['congress'] = congress
            govinfo.run(GOVINFO_OPTIONS)
            processed = bills.run(BILLS_OPTIONS)
