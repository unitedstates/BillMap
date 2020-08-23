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

        with open(TITLES_INDEX_JSON_PATH, 'rb') as f:
            titlesIndex = json.load(f)
    
        context['bill']['meta'] = bill_meta
        bill_summary = deep_get(bill_meta, 'summary', 'text')
        if bill_summary and len(bill_summary) > 200:
            context['bill']['meta']['summary_short'] = bill_summary[0:200] + '...'
        else:
            context['bill']['meta']['summary_short'] = bill_summary
        all_titles = list(set([item.get('title') for item in bill_meta.get('titles')]))
        same_titles = [titlesIndex.get(title) for title in all_titles] 
        same_titles = list(set([item for sublist in same_titles for item in sublist if item != bill]))
        same_titles.sort()
        context['bill']['same_titles'] = ', '.join(same_titles)
        context['bill']['type_abbrev'] = ''.join([letter+'.' for letter in bill_type])
        sponsor_name = deep_get(bill_meta, 'sponsor', 'name').split(', ')
        sponsor_name.reverse()
        context['bill']['sponsor_fullname'] = deep_get(bill_meta, 'sponsor', 'title') + '. ' + ''.join(sponsor_name) + ' ['  'X-' + deep_get(bill_meta, 'sponsor', 'state') + deep_get(bill_meta, 'sponsor', 'district') + ']'
    else:
        return render(request, 'bills/bill.html', context)

    #with open(BILLS_META_JSON_PATH, 'rb') as f:
    #    billsMeta = json.load(f)
    #bill_meta = billsMeta.get(bill)

    return render(request, 'bills/bill.html', context)