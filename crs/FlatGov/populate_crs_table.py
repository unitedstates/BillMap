"""
from FlatGov.populate_crs_table import CrsFromApi
crs = CrsFromApi()
crs.populate()
"""
import re
import math
import json
from FlatGov.models import Bill
from FlatGov.scrapers.everycrsreport_com import EveryCrsReport

# Bill's unique phrases {'sres', 'hjres', 'hconres', 's', 'hres', 'sjres', 'hr', 'sconres'}
BILL_NUMBER_RE = re.compile(
    r'\W(\s?h\s?j\s?res\s?\d+|s\s?res\s?\d+|h\s?con\s?res\s?\d+|h\s?res\s?\d+'
    r'|s\s?j\s?res\s?\d+|h\s?r\s?\d+|s\s?con\s?res\s?\d+)', re.I | re.M)
BILL_NUMBER_S_FOR_TITLE_RE = re.compile(r'\W(S\s?\d+)')
# this is more strict to avoid matches with
# `word ended withs and digit after` or with images like `+s3..`
BILL_NUMBER_S_FOR_TEXT_RE = re.compile(r'\W(S\s?\d{3,4})')


def get_congress_number_for_year(year):
    return math.ceil((int(year) - 1788) / 2)


class CrsFromApi:
    matched_count = 0

    def process_bills_for_report(self, bill_numbers, report, source='title'):
        congress_number = get_congress_number_for_year(report.date[:4])
        for bill_number in bill_numbers:
            bill_id = f'{congress_number}{bill_number}'.replace(' ', '').lower()
            try:
                bill = Bill.objects.get(pk=bill_id)
                print(f'{bill_id} got matched, use existing bill.')
                self.matched_count += 1
            except Bill.DoesNotExist:
                print(f'{bill_id} does not have a matches in Bills. Creating new one.')
                bill = Bill(number=bill_id, titles=json.dumps([report.title]))
            bill.save()
            report.bills.add(bill)

    def populate(self):
        reports_count = extracted_count = 0
        api = EveryCrsReport()
        for report in api.scrape():
            reports_count += 1
            print(report)
            report.save()  # to have an id for many-to-many
            bill_numbers = BILL_NUMBER_RE.findall(report.title.replace('.', '')) + \
                           BILL_NUMBER_S_FOR_TITLE_RE.findall(report.title.replace('.', ''))
            if bill_numbers:
                extracted_count += len(bill_numbers)
                self.process_bills_for_report(bill_numbers, report, source='title')
            if report.report_content_raw:
                bill_numbers = BILL_NUMBER_RE.findall(report.report_content_raw.replace('.', '')) + \
                               BILL_NUMBER_S_FOR_TEXT_RE.findall(report.title.replace('.', ''))
                if bill_numbers:
                    extracted_count += len(bill_numbers)
                    self.process_bills_for_report(bill_numbers, report, source='text')
            report.save()  # call save after all bills will be added
        print(f'{reports_count} reports processed')
        print(f'{extracted_count} bill numbers extracted')
        print(f'{self.matched_count} bills matched')
