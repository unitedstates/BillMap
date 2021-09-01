import os
from typing import Tuple
from django.conf import settings
from elasticsearch import exceptions, Elasticsearch
from common import constants
from common.utils import dumpRelatedBillJSON
from common.billdata import (
    loadJSON,
    billIdToBillNumber,
    getBillCongressTypeNumber,
    getBillTitles,
    getCosponsors,
)
from common.elastic_load import indexBill
from common.bill_similarity import processBill


es = Elasticsearch()
DIR = settings.PATH_TO_CONGRESSDATA_DIR
BILL_JSON = 'data.json'
BILL_XML = 'document.xml'

def get_bill_dir(bill):
    """
    get uscongress bill directory
    eg: 117-hres12 -> .../congress/data/117/bills/hres/hres12
    """
    [bill_type_num, congress] = bill.split('-')
    bill_type = ''.join([i for i in bill_type_num if not i.isdigit()])
    return os.path.join(DIR, congress, 'bills', bill_type, bill_type_num)


def validate_bill_dir(bill_dir, fname):
    for dir_name, sub_dirs, files in os.walk(bill_dir):
        if fname in files:
            return dir_name
    return False


def add_bill_meta(dirName: str, fileName: str):
    related_dict = dict()
    billDict = loadJSON(os.path.join(dirName, fileName))
    try:
        bill_congress_type_number = getBillCongressTypeNumber(billDict)
        if not bill_congress_type_number:
            return False
    except Exception as err:
        return False

    titles = getBillTitles(billDict)
    related_dict['titles'] = [title.get('title') for title in titles]
    related_dict['titles_whole_bill'] = [title.get('title') for title in titles if not title.get('is_for_portion')]
    cosponsors = getCosponsors(fileDict=billDict, includeFields=['name', 'bioguide_id'])
    related_dict['cosponsors'] = cosponsors

    # TODO convert bill_id to billnumber
    related_dict['related_bills'] = billDict.get('related_bills')
    for item in related_dict['related_bills']:
      bill_id = item.get('bill_id') 
      if bill_id:
        item['billCongressTypeNumber'] = billIdToBillNumber(bill_id)
      else:
        item['billCongressTypeNumber'] = None

    dumpRelatedBillJSON(bill_congress_type_number, related_dict)
    return bill_congress_type_number, related_dict


def update_bills_meta(bill: str) -> Tuple[str, dict, bool]:
    bill_dir = get_bill_dir(bill)
    if not validate_bill_dir(bill_dir, BILL_JSON):
        return '', {}, True 
    bill_congress_type_number, related_dict = add_bill_meta(bill_dir, BILL_JSON)
    return bill_congress_type_number, related_dict, False 


def create_es_index(index: str='billsections', body: dict=constants.BILLSECTION_MAPPING):
    indices = es.indices.get_alias().keys()
    if index in indices:
        return False
    es.indices.create(index=index, ignore=400, body=body)
    return True


def es_index_bill(bill):
    print("Indexing" + bill)
    bill_dir = get_bill_dir(bill)
    print("Indexing " + bill + " in " + bill_dir)
    valid_bill_dir = validate_bill_dir(bill_dir, BILL_XML)
    if not valid_bill_dir:
        print("Invalid bill directory")
        return False
    res = indexBill(os.path.join(valid_bill_dir, BILL_XML))
    print("Indexed " + bill)
    print(res)
    return res


def es_similarity_bill(bill):
    bill_dir = get_bill_dir(bill)
    valid_bill_dir = validate_bill_dir(bill_dir, BILL_XML)
    if not valid_bill_dir:
        return False
    res = processBill(os.path.join(valid_bill_dir, BILL_XML))
    return res
