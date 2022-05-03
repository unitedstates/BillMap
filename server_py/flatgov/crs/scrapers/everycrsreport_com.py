import os
import csv
import json
import requests
from urllib.parse import urljoin

from django.conf import settings
from crs.models import CrsReport


class EveryCrsReport:
    SITE_URL = 'https://www.everycrsreport.com'
    REPORTS_API_URL = 'https://www.everycrsreport.com/reports.csv'

    def scrape(self, download_pdf=False):
        """
        Structure of the row: number,url,sha1,latestPubDate,title,latestPDF,latestHTML
        """
        r = requests.get(EveryCrsReport.REPORTS_API_URL)
        if not r:
            raise RuntimeError("Can't get reports from everycrsreport.com")
        reader = csv.DictReader(r.content.decode("utf8").splitlines())

        meta_url_dups = CrsReport.objects.values_list('meta_url', flat=True).distinct()
        html_url_dups = CrsReport.objects.values_list('html_url', flat=True).distinct()

        for row in reader:
            try:
                if urljoin(EveryCrsReport.SITE_URL, row['url']) in meta_url_dups:
                    continue

                r_meta = requests.get(urljoin(EveryCrsReport.SITE_URL, row['url']))
                meta = r_meta.json()
            except requests.exceptions.RequestException:
                meta = None

            try:
                if urljoin(EveryCrsReport.SITE_URL, row['latestHTML']) in html_url_dups:
                    continue

                r_report_html = requests.get(urljoin(EveryCrsReport.SITE_URL, row['latestHTML']))
                report_content_raw = r_report_html.text
                # TODO consider finding the bills here and only storing snippets that can be shown
            except requests.exceptions.RequestException:
                report_content_raw = None

            if download_pdf:
                EveryCrsReport.download_report(row['latestPDF'])
            yield CrsReport(
                title=row['title'],
                file=row['latestPDF'].split('/')[-1],
                date=row['latestPubDate'],
                metadata=json.dumps(meta),
                report_content_raw=report_content_raw,
                meta_url=urljoin(EveryCrsReport.SITE_URL, row['url']),
                html_url=urljoin(EveryCrsReport.SITE_URL, row['latestHTML']),
            )

    @staticmethod
    def download_report(filename):
        r = requests.get(urljoin(EveryCrsReport.SITE_URL, filename), stream=True)
        with open(os.path.join(settings.BASE_DIR, 'crs', filename), 'wb') as fd:
            for chunk in r.iter_content(100000):
                fd.write(chunk)

    @staticmethod
    def extract_summary_from_metadata(meta):
        try:
            return meta['versions'][0]['summary']
        except (IndexError, KeyError):
            return None
