import os
import re
import scrapy
import json

from scrapy.http import Request

PATH_META_DEFAULT = os.path.join('pdf', 'meta.json')

# See https://stackoverflow.com/a/52989487/628748

class sap_pdf_simple(scrapy.Spider):
  name = "sap_download"

  allowed_domains = ['www.whitehouse.gov']
  start_urls = ['https://www.whitehouse.gov/omb/statements-of-administration-policy/']
  
  with open(PATH_META_DEFAULT, 'w') as meta_file:
    json.dump([], meta_file, indent = 4)

  def parse(self, response):
    base_url = 'https://www.whitehouse.gov'

    for selector in response.xpath('//a[@href]'):
        link_text = selector.xpath('./text()').get()
        bill_suffix = ''
        bill_number = ''
        if link_text:
          bill_name = re.sub(r'\s', '', link_text.split('-')[0].strip())
          bill_number = re.sub(r'\.', '', bill_name.split('–')[0].split('—')[0]).replace('and', '')
          self.logger.info('Bill Number: %s',  bill_number)
          bill_suffix = '(' + bill_number + ')'

        self.logger.info('Text: %s',  link_text)
        link = selector.xpath('./@href')[0].extract()

        if link.endswith('.pdf'):

            self.logger.info('Link: %s',  link )
            path = os.path.join('pdf', bill_number.replace(',','-') + '.pdf')
            self.logger.info('Path: %s',  path )
            yield Request(link, callback=self.save_pdf, cb_kwargs=dict(path=path))

            # update metadata
            meta_dict = {"url": response.url, "link": link, "link_text": link_text, "path": path, "bill_number": bill_number}
            self.update_meta(meta_dict)

  def save_pdf(self, response, path):
      with open(path, 'wb') as f:
          f.write(response.body)

  def update_meta(self, meta_dict):
      meta_path = meta_dict.get('meta_path', PATH_META_DEFAULT)
      self.logger.debug('Meta_Dict: %s',  str(meta_dict))
      with open(meta_path, 'r') as meta_read_file:
          meta_current = json.load(meta_read_file)
          meta_current.append(meta_dict)

      with open(meta_path, 'w') as meta_write_file:
          json.dump(meta_current, meta_write_file, indent=4)
      