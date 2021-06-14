import os
from typing import Mapping
from celery import shared_task
from django.db.models.fields import BinaryField


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from committeeReport.models import CommitteeReportScrapyTask

from statementAdminPolicy.spiders.sap_download import SapPdfSimple
from committeeReport.spiders.committeereport import CommitteeReportSpider
from committeeReport.committee_report_scrape_urls import get_detail_urls
from common.cbo import cbo
from common.cosponsor import updateCosponsorAndCommittees
from crs.populate_crs_table import CrsFromApi

@shared_task(bind=True)
def sap_scrapy_task(self):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'statementAdminPolicy.settings')
    process = CrawlerProcess(get_project_settings())
    process.crawl(SapPdfSimple)
    process.start(stop_after_crawl=False)


@shared_task(bind=True)
def committee_report_scrapy_task(self):
    # Create Committee Report Detail Urls to committee_report_detail_urls.json file
    last_task_log = CommitteeReportScrapyTask.objects.first()

    if last_task_log:
        last_congress = last_task_log.congress
    else:
        last_congress = None
    last_congress = get_detail_urls(last_congress)
    task_log = CommitteeReportScrapyTask.objects.create(congress=last_congress)

    # Start Crawling and store data into database
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'committeeReport.settings')
    process = CrawlerProcess(get_project_settings())
    process.crawl(CommitteeReportSpider)
    process.start(stop_after_crawl=False)

@shared_task(bind=True)
def cbo_task(self):
    cbo()


@shared_task(bind=True)
def crs_task(self):
    crs_api = CrsFromApi()
    crs_api.populate()


@shared_task(bind=True)
def update_cosponsor_comm_task(self):
    updateCosponsorAndCommittees()
