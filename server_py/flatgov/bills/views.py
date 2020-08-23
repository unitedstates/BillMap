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
TITLES_INDEX_JSON_PATH = getattr(settings, "TITLES_INDEX_JSON_PATH", None) 

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
        
        with open(BILLS_META_JSON_PATH, 'rb') as f:
            billsMeta = json.load(f)

        with open(TITLES_INDEX_JSON_PATH, 'rb') as f:
            titlesIndex = json.load(f)
    
        context['bill']['meta'] = bill_meta
        bill_summary = deep_get(bill_meta, 'summary', 'text')
        if bill_summary and len(bill_summary) > 200:
            context['bill']['meta']['summary_short'] = bill_summary[0:200] + '...'
        else:
            context['bill']['meta']['summary_short'] = bill_summary
        related_bills_numbers = sorted([billIdToBillNumber(item.get('bill_id')) for item in bill_meta.get('related_bills')])
        context['bill']['related_bills_numbers'] = related_bills_numbers
        related_bills_all_titles = [deep_get(billsMeta, billnumber, 'titles') for billnumber in related_bills_numbers]
        related_bills_all_titles = sorted(list(set([item for sublist in related_bills_all_titles for item in sublist])), key=None)
        related_bills_same_titles = [titlesIndex.get(title) for title in related_bills_all_titles] 
        related_bills_same_titles = sorted(list(set([item for sublist in related_bills_same_titles for item in sublist if item != bill])), key=None)
        context['bill']['related_bills_same_titles'] = related_bills_same_titles


        all_titles = list(set([item.get('title') for item in bill_meta.get('titles')]))
        same_titles = [titlesIndex.get(title) for title in all_titles] 
        same_titles = sorted(list(set([item for sublist in same_titles for item in sublist if item != bill])), key=None)
        context['bill']['same_titles'] = same_titles
        context['bill']['same_titles_text'] = ', '.join(same_titles)
        context['bill']['type_abbrev'] = makeTypeAbbrev(bill_type)
        sponsor_name = cleanSponsorName(deep_get(bill_meta, 'sponsor', 'name'))
        context['bill']['sponsor_fullname'] = deep_get(bill_meta, 'sponsor', 'title') + '. ' + sponsor_name + ' '  + makeSponsorBracket(bill_meta.get('sponsor')) 
    else:
        return render(request, 'bills/bill.html', context)


    return render(request, 'bills/bill.html', context)