import os
from celery import shared_task

from statementAdminPolicy.spiders.sap_download import SapPdfSimple
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

@shared_task(bind=True)
def sap_scrapy_task(self):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'statementAdminPolicy.settings')
    process = CrawlerProcess(get_project_settings())
    process.crawl(SapPdfSimple)
    process.start(stop_after_crawl=False)
