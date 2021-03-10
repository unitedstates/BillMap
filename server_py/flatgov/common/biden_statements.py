import json
import requests
from bills.models import Statement
import os

def load_statements():
    Statement.objects.all().delete()
        
    with open('dumped_statements.json', 'r') as f:
        statements_data =json.loads(f.read())
        print(len(statements_data))
    os.system('./manage.py loaddata dumped_statements.json')
