import scrapy
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
FILE_PATH = os.path.join(BASE_DIR, 'committeeReport', 'commitee_report_detail_urls.json')

class CommitteeReportSpider(scrapy.Spider):
    name = 'committeereport'

    def start_requests(self):
        with open(FILE_PATH, 'r') as urls_file:
            urls = urls_file.read().split('\n')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        committee_report_data = self.get_detail_data(response)
        return committee_report_data

    def get_detail_data(self, response):
        committee_report_data = {}

        data = json.loads(response.text)
        committee_report_data['title'] = data['title']
        committee_report_data['pdf_link'] = data['download']['pdflink']
        for col in data['metadata']['columnnamevalueset']:
            #print(col)
            if col['colname'] == 'Category':
                committee_report_data['category'] = col['colvalue']
            elif col['colname'] == 'Report Type':
                committee_report_data['report_type'] = col['colvalue']
            elif col['colname'] == 'Report Number':
                committee_report_data['report_number'] = col['colvalue']
            elif col['colname'] == 'Date':
                committee_report_data['date'] = ' '.join(col['colvalue'].split())
            elif col['colname'] == 'Committee':
                committee_report_data['committee'] = col['colvalue']
            elif col['colname'] == 'Associated Legislation':
                committee_report_data['associated_legislation'] = col['colvalue']
        return committee_report_data 