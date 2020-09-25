import os
import json
from django.shortcuts import render
from django.conf import settings

CONGRESS_DATA_PATH = getattr(settings, "CONGRESS_DATA_PATH", None) 
BILL_LIST_PATH = os.path.join(CONGRESS_DATA_PATH, 'billList.json')
SAMPLE_BILLS = "['116hr1', '116hr202', '116s200', '112hr100']"

if os.file.exists(BILL_LIST_PATH):
    with open(BILL_LIST_PATH, 'r') as f:
        billsList = json.load(f) 
else:
    billsList = SAMPLE_BILLS 

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from functools import reduce
import json
from typing import Dict


def index(request):
    return HttpResponse("Hello, world. You're at the home index.")

def getBillsList(request):
    context = {}
    context['bill_list'] = billsList 
    return JsonResponse(context)

def home_view(request):
    return render(request, 'home/home.html')