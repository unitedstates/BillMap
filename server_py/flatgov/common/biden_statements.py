import json
import requests
from bills.models import Statement
import os
from django.core.files import File
from django.conf import settings

def load_statements():
    os.chdir('../../scrapers/statementAdminPolicy')
    os.system('scrapy crawl sap_download')
    os.chdir(settings.BASE_DIR)
    statements = Statement.objects.filter(belongs_to='Biden').values('permanent_pdf_link',)

    for statement in statements:
        os.remove(statement['permanent_pdf_link'])
    statements = Statement.objects.filter(belongs_to='Biden').delete()

    with open('biden_data.json', 'r') as f:
        statements_data =json.loads(f.read())
        for i, meta_statement in enumerate(statements_data):
            statement = Statement()
            statement.bill_id = str(meta_statement['congress']) + str(meta_statement['bill_number']).lower()
            statement.bill_title = meta_statement['link_text']
            statement.congress = meta_statement['congress']
            statement.date_issued = meta_statement['date_issued']
            statement.original_pdf_link = meta_statement['link']
            statement.bill_number = meta_statement['bill_number']
            statement.belongs_to = 'Biden'
            response = requests.get(meta_statement['link'], stream = True)
            statement.permanent_pdf_link = File(response.raw, name=f"{settings.MEDIA_ROOT}/statements/{statement.congress}/{statement.bill_number}/{meta_statement['link'].split('/')[-1]}")
            statement.save()
            print(i, statement)

            