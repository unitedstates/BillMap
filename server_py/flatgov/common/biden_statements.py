import requests
import yaml

from bills.models import Statement


def load_biden_statements():
    current_biden_statements = Statement.objects.filter(administration='Biden')
    url = 'https://raw.githubusercontent.com/unitedstates/statements-of-administration-policy/main/archive/46-Biden.yaml'
    original_pdf_path = 'https://github.com/unitedstates/statements-of-administration-policy/tree/main/archive/'
    response = requests.get(url)
    response_data = yaml.safe_load(response.text)
    if current_biden_statements.count() >= len(response_data):
        print("There're no any new biden statement to process.")
        return True
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
        statement.permanent_pdf_link = original_pdf_path + meta_statement['file']
        statement.save()
        print(i, statement)
