import os
from django.conf import settings
from common import constants
from common.utils import dumpRelatedBillJSON
from common.billdata import (
    loadJSON,
    billIdToBillNumber,
    getBillCongressTypeNumber,
    getBillTitles,
    getCosponsors,
)

DIR = settings.PATH_TO_CONGRESSDATA_DIR
BILL_XML = 'data.json'

def get_bill_dir(bill):
    """
    get uscongress bill directory
    eg: 117-hres12 -> .../congress/data/117/bills/hres/hres12
    """
    [bill_type_num, congress] = bill.split('-')
    bill_type = ''.join([i for i in bill_type_num if not i.isdigit()])
    return os.path.join(DIR, congress, 'bills', bill_type, bill_type_num)


def validate_bill_dir(bill_dir):
    files = os.listdir(bill_dir)
    return True if BILL_XML in files else False


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


def update_bills_meta(bill):
    bill_dir = get_bill_dir(bill)
    if not validate_bill_dir(bill_dir):
        return False
    bill_congress_type_number, related_dict = add_bill_meta(bill_dir, BILL_XML)
    return bill_congress_type_number, related_dict
