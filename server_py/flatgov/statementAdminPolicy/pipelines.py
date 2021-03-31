# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import requests
from itemadapter import ItemAdapter
from django.core.files import File
from bills.models import Statement


class StatementadminpolicyPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_item(self, item, spider):
        try:
            response = requests.get(item['link'], stream = True)
            statement = Statement(
                bill_id=str(item['congress']) + str(item['bill_number']).lower(),
                bill_title=item['link_text'],
                congress=item['congress'],
                date_issued=item['date_issued'],
                original_pdf_link=item['link'],
                bill_number=item['bill_number'],
                administration='Biden',
                permanent_pdf_link=File(
                    response.raw, name=f"{item['congress']}/{item['bill_number']}/{item['link'].split('/')[-1]}"
                ),
                request_url=item['request_url'],
            )
        
            statement.save()
        except Exception as e:
            pass

        return item
