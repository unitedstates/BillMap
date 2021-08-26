import json
import requests
from bills.models import Statement
import os
from django.core.files import File
from django.conf import settings
import yaml

def load_biden_statements():
    current_biden_statements = Statement.objects.filter(administration='Biden')
    url = 'https://raw.githubusercontent.com/unitedstates/statements-of-administration-policy/main/archive/46-Biden.yaml'
    response = requests.get(url)
    response_data = yaml.safe_load(response.text)
    if current_biden_statements.count() >= len(response_data):
        print("There're no any new biden statement to process.")
        return True

    os.chdir(settings.BASE_DIR)
    statement_pdf_links = current_biden_statements.values('permanent_pdf_link',)

    for statement_pdf_link in statement_pdf_links:
        try:
            os.remove(settings.MEDIA_ROOT / statement_pdf_link['permanent_pdf_link'])
        except OSError:
            pass
    current_biden_statements.delete()

    for i, meta_statement in enumerate(response_data):
        statement = Statement()
        statement.bill_id = str(meta_statement['congress']) + str(meta_statement['bills'][0]).lower()
        statement.bill_title = meta_statement['document_title']
        statement.congress = meta_statement['congress']
        statement.date_issued = meta_statement['date_issued']
        statement.original_pdf_link = meta_statement['fetched_from_url']
        statement.bill_number = meta_statement['bills'][0]
        statement.administration = 'Biden'
        response = requests.get(meta_statement['fetched_from_url'], stream = True)
        statement.permanent_pdf_link = File(response.raw, name=f"{statement.congress}/{statement.bill_number}/{meta_statement['fetched_from_url'].split('/')[-1]}")
        statement.save()
        print(i, statement)
