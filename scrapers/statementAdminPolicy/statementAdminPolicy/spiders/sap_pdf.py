import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class SapPdfSpider(CrawlSpider):
    name = 'sap_pdf'
    allowed_domains = ['www.whitehouse.gov']
    start_urls = ['https://www.whitehouse.gov/omb/statements-of-administration-policy/']

    rules = (
         Rule(LinkExtractor(allow=r'/wp-content'), callback='parse_item', follow=True),
     )

    def parse_item(self, response):
        if re.match(r'.*content', response.url):
            self.logger.info('Downloading: %s', response.url)
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
