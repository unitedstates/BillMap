"""
Use to populate:

from crs.populate_crs_table import CrsFromApi
crs_api = CrsFromApi()
crs_api.populate()
"""
import re
import math
import json
from bills.models import Bill
from crs.scrapers.everycrsreport_com import EveryCrsReport

# Bill's types {'sres', 'hjres', 'hconres', 's', 'hres', 'sjres', 'hr', 'sconres'}
BILL_NUMBER_RE = re.compile(
    r'\W(\s?h\s?j\s?res\s?\d+|s\s?res\s?\d+|h\s?con\s?res\s?\d+|h\s?res\s?\d+'
    r'|s\s?j\s?res\s?\d+|h\s?r\s?\d+|s\s?con\s?res\s?\d+)', re.I | re.M)
BILL_NUMBER_S_FOR_TITLE_RE = re.compile(r'\W(S\s?\d+)')

# this is more strict to avoid matches with
# `word ended with S and digit after` or with images like `+s3..`
BILL_NUMBER_S_FOR_TEXT_RE = re.compile(r'\W(S\s?\d{3,4})')


def get_congress_number_for_year(year: str) -> int:
    return math.ceil((int(year) - 1788) / 2)


class CrsFromApi:
    matched_count = 0
    extracted_count = 0

    def process_bills_for_report(self, bill_numbers, report, source='title'):
        congress_number = get_congress_number_for_year(report.date[:4])
        # construct IDs and remove duplicates
        bill_ids = set()
        for bill_number in bill_numbers:
            bill_id = f'{congress_number}{bill_number}'.replace(' ', '')\
                .replace('\n', '').lower()
            bill_ids.add(bill_id)

            # Add prior year if report was in January or February
            if int(report.date[5:7]) < 3:
                bill_id = f'{congress_number-1}{bill_number}'.replace(' ', '')\
                .replace('\n', '').lower()
                bill_ids.add(bill_id)

        self.extracted_count += len(bill_ids)
        for bill_id in bill_ids:
            try:
                bill = Bill.objects.get(bill_congress_type_number=bill_id)
                print(f'{bill_id} was matched, use existing bill.')
                self.matched_count += 1
            except Bill.DoesNotExist:
                print(f'{bill_id} does not have a match in Bills. Creating new one.')
                bill_type = re.search(r'([a-z]+)(\d+)', bill_id)[1]
                bill = Bill(
                    type=bill_type,
                    number=re.search(r'([a-z]+)(\d+)', bill_id)[2],
                    congress=congress_number,
                    bill_congress_type_number=bill_id,
                    titles=json.dumps([report.title]),
                    es_similarity=json.dumps([]),
                    es_similar_bills_dict=json.dumps({})
                )
            bill.save()
            report.bills.add(bill)

    def populate(self):
        reports_count = 0
        api = EveryCrsReport()
        for report in api.scrape():
            reports_count += 1
            print(report)
            report.save()
            bill_numbers = BILL_NUMBER_RE.findall(report.title.replace('.', '')) + \
                           BILL_NUMBER_S_FOR_TITLE_RE.findall(report.title.replace('.', ''))
            if bill_numbers:
                self.process_bills_for_report(bill_numbers, report, source='title')
            if report.report_content_raw:
                bill_numbers = BILL_NUMBER_RE.findall(report.report_content_raw.replace('.', '')) + \
                               BILL_NUMBER_S_FOR_TEXT_RE.findall(report.report_content_raw.replace('.', ''))
                if bill_numbers:
                    self.process_bills_for_report(bill_numbers, report, source='text')
            report.save()  # call save after all bills will be added
        print(f'{reports_count} reports processed')
        print(f'{self.extracted_count} bill numbers extracted')
        print(f'{self.matched_count} bills matched')
