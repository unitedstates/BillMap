"""
from FlatGov.scrapers.everycrsreport_com import EveryCrsReport
api = EveryCrsReport()
api.scrape()

"""
import csv
import json
import requests
from urllib.parse import urljoin

from FlatGov.models import CrsReport


class EveryCrsReport:
    SITE_URL = 'https://www.everycrsreport.com'
    REPORTS_API_URL = 'https://www.everycrsreport.com/reports.csv'

    def scrape(self):
        """
        Structure of the row: number,url,sha1,latestPubDate,title,latestPDF,latestHTML
        """
        r = requests.get(EveryCrsReport.REPORTS_API_URL)
        if not r:
            raise RuntimeError("Can't get reports from everycrsreport.com")
        reader = csv.DictReader(r.text.splitlines())
        for row in reader:
            try:
                r_meta = requests.get(urljoin(EveryCrsReport.SITE_URL, row['url']))
                meta = r_meta.json()
            except requests.exceptions.RequestException:
                meta = None

            try:
                r_report_html = requests.get(urljoin(EveryCrsReport.SITE_URL, row['latestHTML']))
                report_content_raw = r_report_html.text
            except requests.exceptions.RequestException:
                report_content_raw = None

            EveryCrsReport.download_report(row['latestPDF'])
            yield CrsReport(
                title=row['title'],
                file=row['latestPDF'].split('/')[-1],
                date=row['latestPubDate'],
                metadata=json.dumps(meta),
                report_content_raw=report_content_raw
            )

    @staticmethod
    def download_report(filename):
        r = requests.get(urljoin(EveryCrsReport.SITE_URL, filename), stream=True)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(100000):
                fd.write(chunk)

    @staticmethod
    def extract_summary_from_metadata(meta):
        try:
            return meta['versions'][0]['summary']
        except (IndexError, KeyError):
            return None
