import os
import json
from functools import reduce
from typing import Dict
from operator import itemgetter

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from django_tables2 import MultiTableMixin

from common.elastic_load import getSimilarSections, moreLikeThis, getResultBillnumbers, getInnerResults

from bills.models import Bill, Cosponsor, Statement

from bills.serializers import RelatedBillSerializer, CosponsorSerializer

from crs.models import CrsReport

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
    if not lastfirst:
        return ''
    else:
        return ' '.join(reversed(lastfirst.split(', ')))


def makeTypeAbbrev(bill_type) -> str:
    return ''.join([letter+'.' for letter in bill_type])


def makeSponsorBracket(sponsor: dict, party='X') -> str:
    # TODO: in the future, make party required 
    state = sponsor.get('state', '')
    if not state:
        state = ''
    district =  sponsor.get('district', '')
    # Implemented this because default of '' does not seem to work
    if not district:
        district = ''

    return '[' + party + '-' +  state + district + ']'


class BillListView(TemplateView):
    template_name = 'bills/list.html'

    def get_context_data(self, **kwargs):
        from uscongress.tasks import bill_similarity_task
        bill_similarity_task(26)
        context = super().get_context_data(**kwargs)
        return context


def makeName(commaName):
    if not commaName:
        return ''
    return ' '.join(reversed(commaName.split(',')))


def similar_bills_view(request):
    noResults = False
    # after the redirect (in the views.py that handles your redirect)
    queryText = request.session.get('queryText')
    if not queryText:
        queryText = ''
    res = moreLikeThis(queryText = queryText) 
    similarBillNumbers = getResultBillnumbers(res)
    similarSections = sorted(getSimilarSections(res), key=itemgetter('score'), reverse=True)
    bestMatch = {}
    if not similarSections or len(similarSections) == 0:
        noResults = True 
    else:
        bestMatch = similarSections[0]
    
    context = {
        "billQuery": {
            "queryText": queryText,
            "bestMatch": bestMatch,
            "similarBillNumbers": similarBillNumbers,
            "similarSections": json.dumps(similarSections), 
            "noResults": noResults
        }
    }
    return render(request, 'bills/bill-similar.html', context)
class BillDetailView(DetailView):
    model = Bill
    template_name = 'bills/detail.html'
    slug_field = 'bill_congress_type_number'
    # paginate_by = settings.DJANGO_TABLES2_PAGINATE_BY

    def get_qs_related_bill(self):
        congress_list = self.object.get_related_bill_numbers()
        qs = Bill.objects.filter(bill_congress_type_number__in=congress_list)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cosponsors'] = self.get_cosponsors()
        context['statements'] = self.get_related_statements()
        context['crs_reports'] = self.get_crs_reports()
        context['related_bills'] = self.get_related_bills()
        context['similar_bills'] = self.object.get_similar_bills
        context['es_similarity'] = self.object.es_similarity
        return context

    
    def get_related_statements(self, **kwargs):
        slug = self.kwargs['slug']
        return Statement.objects.filter(bill_number__iexact=slug[3:]).filter(congress__iexact=slug[:3])

    def get_crs_reports(self, **kwargs):
        slug = self.kwargs['slug']
        return self.object.crsreport_set.all()
        
    def get_related_bills(self):
        qs = self.get_qs_related_bill()
        serializer = RelatedBillSerializer(
            qs, many=True, context={'bill': self.object})
        return serializer.data

    def get_cosponsors(self):
        cosponsor_ids = list(self.object.cosponsors.values_list('pk', flat=True))
        sponsor_name = self.object.sponsor.get('name')
        if sponsor_name:
            sponsor_id = Cosponsor.objects.filter(name=sponsor_name).first().pk
            cosponsor_ids.append(sponsor_id)
        qs = Cosponsor.objects.filter(pk__in=cosponsor_ids)
        serializer = CosponsorSerializer(
            qs, many=True, context={'bill': self.object})
        return serializer.data


class BillToBillView(DetailView):
    model = Bill
    template_name = 'bills/compare.html'
    slug_field = 'bill_congress_type_number'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        second_bill = self.kwargs.get('second_bill')
        context['second_bill'] = Bill.objects.get(bill_congress_type_number=second_bill)
        context['bill_to_bill'] = self.object.es_similar_bills_dict.get(second_bill, [])
        return context
