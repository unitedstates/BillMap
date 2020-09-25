import os
from django.shortcuts import render
from django.conf import settings

CONGRESS_DATA_PATH = getattr(settings, "CONGRESS_DATA_PATH", None) 
BILL_LIST_PATH = os.path.join(CONGRESS_DATA_PATH, 'billList.json')

with open(BILL_LIST_PATH, 'r') as f:
    billsList = f.read() 

# Create your views here.

from django.http import HttpResponse
from django.conf import settings
from functools import reduce
import json
from typing import Dict


def index(request):
    return HttpResponse("Hello, world. You're at the home index.")

def home_view(request):
    context = {'bill_list': billsList}
    return render(request, 'home/home.html', context)