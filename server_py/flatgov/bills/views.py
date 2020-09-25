import os
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.conf import settings
from functools import reduce
import json
from typing import Dict


def deep_get(dictionary: Dict, *keys):
  """
  A Dict utility to get a field; returns None if the field does not exist

  Args:
      dictionary (Dict): an arbitrary dictionary 

  Returns:
      any: value of the specified key, or None if the field does not exist
  """

  return reduce(
    lambda d, key: d.get(key, None) if isinstance(d, dict) else None, keys, 
    dictionary)

CONGRESS_DATA_PATH = getattr(settings, "CONGRESS_DATA_PATH", None) 
BILLS_META_JSON_PATH = getattr(settings, "BILLS_META_JSON_PATH", None) 
RELATED_BILLS_JSON_PATH = getattr(settings, "RELATED_BILLS_JSON_PATH", None) 
TITLES_INDEX_JSON_PATH = getattr(settings, "TITLES_INDEX_JSON_PATH", None) 
with open(RELATED_BILLS_JSON_PATH, 'rb') as f:
    relatedBillsAll = json.load(f)

import re

BILL_REGEX = r'([1-9][0-9]{2})([a-z]+)(\d+)'

# Utilities. These should go in a utils.py module
def billIdToBillNumber(bill_id: str) -> str:
    """
    Converts a bill_id of the form `hr299-116` into `116hr299`

    Args:
        bill_id (str): hyphenated bill_id from bill status JSON

    Returns:
        str: billCongressTypeNumber (e.g. 116hr299) 
    """
    # TODO test if it has the right form, otherwise throw an exception
    return ''.join(reversed(bill_id.split('-')))

def cleanSponsorName(lastfirst: str) -> str:
    """
    Takes a name of the form "Last, First" and returns "First Last"

    Args:
        lastfirst (str): a string of the form "Last, First" 

    Returns:
        str: a string of the form "First Last" 
    """
    return ' '.join(reversed(lastfirst.split(', ')))

def makeTypeAbbrev(bill_type) -> str:
    return ''.join([letter+'.' for letter in bill_type])

def makeSponsorBracket(sponsor: dict, party='X') -> str:
    # TODO: in the future, make party required 
    return '[' + party + '-' +  sponsor.get('state') + sponsor.get('district') + ']'

def index(request):
    return HttpResponse("Hello, world. You're at the bills index.")

def makeName(commaName):
    if not commaName:
        return ''
    return ' '.join(reversed(commaName.split(',')))

def bill_view(request, bill):
    context = {'billCongressTypeNumber': bill, 'bill': {}}

    bill_parts = re.match(BILL_REGEX, bill)
    if bill_parts:
        bill_parts = list(bill_parts.groups())
        congress = bill_parts[0]
        bill_type = bill_parts[1].upper()
        context['bill']['type'] = bill_type
        bill_number = bill_parts[2]
        BILLMETA_PATH = os.path.join(CONGRESS_DATA_PATH, congress, 'bills', bill_type.lower(), bill_type.lower() + bill_number, 'data.json')
        with open(BILLMETA_PATH, 'rb') as f:
            bill_meta = json.load(f)
        
        relatedBills = deep_get(relatedBillsAll, bill, 'related')
    
        context['bill']['meta'] = bill_meta
        bill_summary = deep_get(bill_meta, 'summary', 'text')
        if bill_summary and len(bill_summary) > 200:
            context['bill']['meta']['summary_short'] = bill_summary[0:200] + '...'
        else:
            context['bill']['meta']['summary_short'] = bill_summary
        bctns = relatedBills.keys()
        context['bill']['related_bill_numbers'] = ', '.join(bctns)

        relatedTable = []
        for bctn in bctns:
            relatedTableItem = relatedBills.get(bctn)
            relatedTableItem['billCongressTypeNumber'] = bctn
            # TODO handle the same bill number (maybe put it at the top?)
            if bill == bctn:
                relatedTableItem['reason'] = 'identical'
            titles = deep_get(relatedBills, bctn, 'titles')
            if titles:
                relatedTableItem['titles_list'] = ", ".join(titles)
            else:
                relatedTableItem['titles_list'] = ""

            titles_year = deep_get(relatedBills, bctn, 'titles_year')
            if titles_year:
                relatedTableItem['titles_year_list'] = ", ".join(titles_year)
            else:
                relatedTableItem['titles_year_list'] = ""
            relatedTableItem['sponsor_name'] = makeName(deep_get(relatedBills, bctn, 'sponsor', 'name'))
            cosponsors = deep_get(relatedBills, bctn, 'cosponsors')
            if cosponsors:
                relatedTableItem['cosponsor_names'] = ", ".join(list(map(lambda item: makeName(item.get('name')), cosponsors)))
            else:
                relatedTableItem['cosponsor_names'] = ''
            relatedTable.append(relatedTableItem)
            
        context['bill']['related_table'] =  json.dumps(relatedTable)

        context['bill']['type_abbrev'] = makeTypeAbbrev(bill_type)
        sponsor_name = cleanSponsorName(deep_get(bill_meta, 'sponsor', 'name'))
        context['bill']['sponsor_fullname'] = deep_get(bill_meta, 'sponsor', 'title') + '. ' + sponsor_name + ' '  + makeSponsorBracket(bill_meta.get('sponsor')) 
    else:
        return render(request, 'bills/bill.html', context)


    return render(request, 'bills/bill.html', context)