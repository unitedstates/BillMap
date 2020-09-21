import os
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.conf import settings
from functools import reduce
import json
from typing import Dict


def index(request):
    return HttpResponse("Hello, world. You're at the home index.")

def home_view(request):
    return render(request, 'home/home.html')