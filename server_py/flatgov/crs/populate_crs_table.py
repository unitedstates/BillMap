"""
Use to populate:

from crs.populate_crs_table import CrsFromApi
crs_api = CrsFromApi()
crs_api.populate()
"""
import re
import math
from bills.models import Bill
from crs.scrapers.everycrsreport_com import EveryCrsReport

# Bill's types {'sres', 'hjres', 'hconres', 's', 'hres', 'sjres', 'hr', 'sconres'}
BILL_NUMBER_RE = re.compile(r"\W((?:h\.\s?r\.|s\.|h\.conres\.|s\.conres\.|h\.\s?j\.\s?res\.|s\.\s?j\.\s?res\.|" 
+ r"h\.\s?res\.|s\.\s?res\.)\s?(?:[1-9]\d{0,3}))", re.I | re.M)

def cleanBillNumber(billnumber):
    return billnumber.replace('.', '').replace(' ', '').lower()

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
                print(f'{bill_id} does not have a match in Bills.')
                # Do no create bill if it is not found in db
                continue
            bill.save()
            report.bills.add(bill)

    def populate(self):
        reports_count = 0
        api = EveryCrsReport()
        for report in api.scrape():
            reports_count += 1
            print(report)
            report.save()
            bill_numbers = map(cleanBillNumber, BILL_NUMBER_RE.findall(report.title))
            if bill_numbers:
                self.process_bills_for_report(bill_numbers, report, source='title')
            if report.report_content_raw:
                bill_numbers = map(cleanBillNumber, BILL_NUMBER_RE.findall(report.report_content_raw))
                if bill_numbers:
                    self.process_bills_for_report(bill_numbers, report, source='text')
            report.save()  # call save after all bills will be added
        print(f'{reports_count} reports processed')
        print(f'{self.extracted_count} bill numbers extracted')
        print(f'{self.matched_count} bills matched')