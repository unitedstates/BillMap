import json
import os

from bills.models import Statement


def load_statements():
    print(Statement.objects.all().count())
    Statement.objects.all().delete()

    with open('dumped_statements.json', 'r') as f:
        statements_data =json.loads(f.read())
        print(len(statements_data))
    os.system('./manage.py loaddata dumped_statements.json')
