import os
import json
import requests
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
from celery import states

from common.elastic_load import getSimilarSections, moreLikeThis, getResultBillnumbers, getInnerResults

from bills.models import (
    Bill, Cosponsor, Statement, CboReport, CommitteeDocument,
    PressStatementTask, PressStatement
)

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
        #from uscongress.tasks import bill_similarity_task
        #bill_similarity_task(26)
        context = super().get_context_data(**kwargs)
        return context

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
        context['cosponsors_dict'] = self.get_cosponsors_dict()
        context['cosponsors'] = self.get_cosponsors()
        context['statements'] = self.get_related_statements()
        context['committees'] = self.get_related_committees()
        context['crs_reports'] = self.get_crs_reports()
        context['cbo_reports'] = self.get_related_cbo()
        context['related_bills'] = self.get_related_bills()
        context['similar_bills'] = self.object.get_similar_bills
        context['es_similarity'] = self.object.es_similarity
        context['propublica_api_key'] = settings.PROPUBLICA_CONGRESS_API_KEY
        return context

    def get_related_statements(self, **kwargs):
        slug = self.kwargs['slug']
        return Statement.objects.filter(bill_number__iexact=slug[3:]).filter(congress__iexact=slug[:3])

    def get_related_committees(self, **kwargs):
        slug = self.kwargs['slug']
        return CommitteeDocument.objects.filter(bill_number__iexact=slug[3:]).filter(congress__iexact=slug[:3])

    def get_crs_reports(self, **kwargs):
        slug = self.kwargs['slug']
        crs_reports = list(self.object.crsreport_set.all())
        crs_reports_context = []
        for report in crs_reports:
            context_item = {"title": report.title, "date": report.date}
            metadata = json.loads(report.metadata)
            versions = metadata.get('versions', [])
            if versions and len(versions) > 0:
                context_item["link"] = versions[0].get('sourceLink', '')
            crs_reports_context.append(context_item)
        return crs_reports_context 
        
    def get_related_cbo(self, **kwargs):
        slug = self.kwargs['slug']
        return CboReport.objects.filter(bill_number__iexact=slug[3:]).filter(congress__iexact=slug[:3])

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

    
    def get_cosponsors_dict(self):
        cosponsors =  self.object.cosponsors_dict
        print(cosponsors)
        cosponsors = sorted(cosponsors, key = lambda i: i.get('name'))

        sponsor = self.object.sponsor
        sponsor['sponsor'] = True
        sponsor_name = sponsor.get('name', '')
        print(sponsor_name)
        if sponsor_name:
            sponsors = [] 
            try:
                sponsors = list(filter(lambda cosponsor: cosponsor.get('name', '') == sponsor_name, cosponsors))
            except Exception as err:
                pass
            if sponsors:
                print(sponsors[0])
                cosponsors.remove(sponsors[0])
                cosponsors.insert(0, sponsors[0])
            else:
                cosponsors.insert(0, sponsor)
        return cosponsors

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
