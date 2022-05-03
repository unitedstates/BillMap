import json
import os
from pathlib import Path

import scrapy

from bills.models import CommitteeDocument

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
FILE_PATH = os.path.join(BASE_DIR, 'commitee_report_detail_urls.json')


class CommitteeReportSpider(scrapy.Spider):
    name = 'committeereport'

    def start_requests(self):
        with open(FILE_PATH, 'r') as urls_file:
            urls = urls_file.read().split('\n')
        registered_urls = CommitteeDocument.objects.values_list('request_url', flat=True).distinct()
        start_urls = set(filter(None, urls)) - set(registered_urls)
        for url in start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        committee_report_data = self.get_detail_data(response)
        yield committee_report_data

    def get_detail_data(self, response):
        committee_report_data = {}

        data = json.loads(response.text)
        committee_report_data['title'] = data['title']
        committee_report_data['pdf_link'] = data['download']['pdflink']
        for col in data['metadata']['columnnamevalueset']:
            # print(col)
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
        committee_report_data['request_url'] = response.request.url
        return committee_report_data
