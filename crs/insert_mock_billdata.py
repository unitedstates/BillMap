import json
from insert_bill import insert_bill

def insert_mock_billdata():
    bill_json_fn = 'billsMeta.json'
    with open(bill_json_fn) as f:
        jsondata = json.load(f)
        bill_numbers = [(bill,) for bill in list(jsondata.keys())]
        print("bulk inserting...")
        insert_bill(bill_numbers)
        print("bulk inserting is finished")

insert_mock_billdata()