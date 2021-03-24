import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View

from rest_framework.generics import ListAPIView
from common.constants import START_CONGRESS, CURRENT_CONGRESS

from home.forms import QueryForm
from bills.models import Bill
from bills.serializers import BillNumberListSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the home index.")


def home_view(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            queryText = cd.get('queryText')
        else:
            queryText = ''
        request.session['queryText'] = queryText 
        return redirect('/bills/similar')
    else:
        form = QueryForm()
    
    context = {'form': form, 'congressrange': list(reversed(list(range(START_CONGRESS, CURRENT_CONGRESS +1))))}
    return render(request, 'home/home.html', context)


class BillListAPIView(View):
    
    def get(self, request):
        bills = Bill.objects.values_list('bill_congress_type_number', flat=True) \
            .order_by('bill_congress_type_number')
        return JsonResponse({"bill_list": list(bills)})
