# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
from bills.models import CommitteeDocument


class CommitteereportPipeline:
    def process_item(self, item, spider):
        try:
            crec = CommitteeDocument(
                title=item.get('title'),
                category=item.get('category'),
                committee=item.get('committee'),
                report_number=''.join(item.get('report_number').split('&nbsp;')),
                associated_legislation=''.join(item.get('associated_legislation').split('&nbsp;')),
                original_pdf_link=item.get('pdf_link'),
                bill_number=re.sub('\ |\?|\.|\!|\/|\;|\:|\-|\(|\)', '', ''.join(item.get('associated_legislation').split('&nbsp;'))).lower(),
                chamber=item.get('report_type').split()[0],
                report_type=item.get('report_type'),
                date=item.get('date'),
                congress=self.get_congress_number(item.get('date')),
                request_url=item.get('request_url'),
            )
            crec.save()
        except Exception as e:
            pass
        return item

    def get_congress_number(self, date):
        year = date.split()[-1]

        congress = 0
        const_year = 2022
        const_congress = 117
        dif = const_year - int(year)
        congress = const_congress - (dif // 2)
        return congress
