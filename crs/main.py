from insert_crs import insert_crs
from fetch_bill_numbers import fetch_bill_numbers
from extract_congress_number import extract_congress_number
import urllib.request
import csv
import io
import json
import re

# bill_number_re = re.compile('(?P<bill_number>(H\.?R|Res)\.?\s?\d+)', re.I|re.M)

if __name__ == '__main__':

    api_base_url = "https://www.everycrsreport.com/"

    with urllib.request.urlopen(api_base_url + "reports.csv") as resp:
        reader = csv.DictReader(io.StringIO(resp.read().decode("utf8")))

    bill_numbers = fetch_bill_numbers()

    for bill_number in bill_numbers:
         # if bill_number = '116hr2000', congress_number = 116, report_string = hr2000
        congress_number = extract_congress_number(bill_number[1])['congress_number'] 
        report_string = extract_congress_number(bill_number[1])['report_string']

        congress_year = int(congress_number)*2 + 1788
        
        for report in reader:
            report_title = report["title"].replace(' ', '').replace('.', '').lower()
            report_year = report["latestPubDate"].split('-')[0]

            # bill_number = bill_number_re.search(report['title'])
            # if bill_number:
            #     print(bill_number.group('bill_number'))
            #     print(report['title'])

            if report_string in report_title:
                if int(report_year) == congress_year:
                    bill_id = bill_number[0]
                    title = report["title"]
                    date = report["latestPubDate"]
                    link = "reports/" + report["latestPDF"]
                    print('---save to db---', bill_id, title, date, link)
                    
                    # This needs to include the bill_id, if there is one
                    insert_crs(title, date, link)