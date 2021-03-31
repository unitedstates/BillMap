import re
import scrapy
from bs4 import BeautifulSoup as bs4


# See https://stackoverflow.com/a/52989487/628748

class SapPdfSimple(scrapy.Spider):
	name = "sap_download"

	allowed_domains = ['www.whitehouse.gov']
	start_urls = ['https://www.whitehouse.gov/omb/statements-of-administration-policy/']

	def parse(self, response):
		soup = bs4(response.text, 'html.parser')

		con = soup.find('section', {'class': 'body-content'})
		con = con.find('div', {'class': 'row'})
		ps = con.findAllNext('p')[1:]
		new_meta = {
			'url': '',
			'link': '',
			'link_text': '',
			'bill_number': '',
			'date_issued': '',
			'congress': '',
		}

		for i in range(len(ps)):
			try:
				new_meta['date_issued'] = ps[i].text.split('(')[-2].split(')')[0]
				new_meta['link'] = ps[i].find('a', href=True)['href']
				year = new_meta['date_issued'][-4:]
				a_text = ps[i].find('a').text
				new_meta['link_text'] = a_text
				q = re.sub(r'\s', '', a_text.split('–')[0])
				qw = re.sub(r'\.', '', q)
				new_meta['bill_number'] = qw.split('—')[0]
				new_meta['congress'] = self.get_congress_number(year)
				new_meta['url'] = response.request.url
				new_meta['request_url'] = response.request.url
				yield new_meta
			except Exception as e:
				continue

	def get_congress_number(self, year):
		congress = 0
		const_year = 2022
		const_congress = 117
		dif = const_year - int(year)
		congress = const_congress - (dif // 2)
		return congress

	@classmethod
	def update_settings(cls, settings):
		settings.setdict(cls.custom_settings or {}, priority='spider')

from scrapy.settings import Settings
