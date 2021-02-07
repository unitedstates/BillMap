import json
from FlatGov.models import Bill


def bills_to_db(**kwargs):
    if Bill.objects.count() == 0:
        with open('billsMeta.json', 'r') as f:
            bills = json.load(f)
            for number, info in bills.items():
                Bill.objects.create(number=number, titles=json.dumps(info['titles']))
