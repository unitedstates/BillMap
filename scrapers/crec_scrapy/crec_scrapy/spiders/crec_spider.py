import scrapy
import json
import os

class CommitteeSpider(scrapy.Spider):
    name = 'crec'

    def start_requests(self):
        if os.path.exists("data/crec_data.json"):
            os.remove("data/crec_data.json")

        with open('../crec_detail_urls.json', 'r') as urls_file:
            urls = urls_file.read().split('\n')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'data/crec_data.json'
        with open(filename, 'a+') as crec_file:
            crec_data = self.get_detail_data(response)
            json.dump(crec_data, crec_file, indent=4)
        self.log('Saved to '+filename)

    def get_detail_data(self, response):
        crec_data = {}

        data = json.loads(response.text)
        crec_data['title'] = data['title']
        crec_data['pdf_link'] = data['download']['pdflink']
        for col in data['metadata']['columnnamevalueset']:
            #print(col)
            if col['colname'] == 'Category':
                crec_data['category'] = col['colvalue']
            elif col['colname'] == 'Report Type':
                crec_data['report_type'] = col['colvalue']
            elif col['colname'] == 'Report Number':
                crec_data['report_number'] = col['colvalue']
            elif col['colname'] == 'Date':
                crec_data['date'] = ' '.join(col['colvalue'].split())
            elif col['colname'] == 'Committee':
                crec_data['committee'] = col['colvalue']
            elif col['colname'] == 'Associated Legislation':
                crec_data['associated_legislation'] = col['colvalue']
        return crec_data 