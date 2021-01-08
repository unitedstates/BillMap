import os
import scrapy

from scrapy.http import Request

# See https://stackoverflow.com/a/52989487/628748

class sap_pdf_simple(scrapy.Spider):
  name = "sap_pdf_simple"

  allowed_domains = ['www.whitehouse.gov']
  start_urls = ['https://www.whitehouse.gov/omb/statements-of-administration-policy/']

  def parse(self, response):
    base_url = 'https://www.whitehouse.gov'

    for selector in response.xpath('//a[@href]'):
        link_text = selector.xpath('./text()').get()
        bill_suffix = ''
        if link_text:
          bill_name = link_text.split('-')[0].strip()
          bill_suffix = '/(' + bill_name + ')'

        self.logger.info('Text: %s',  link_text)
        link = selector.xpath('./@href')[0].extract()

        if link.endswith('.pdf'):

            self.logger.info('Link: %s',  link )
            #link = link.replace('.pdf', bill_suffix + '.pdf')

            yield Request(link, callback=self.save_pdf)

  def save_pdf(self, response):
    path = os.path.join('pdf', '-'.join(response.url.split('/')[2:]))
    self.logger.info('Saving PDF %s', path)
    with open(path, 'wb') as f:
        f.write(response.body)
