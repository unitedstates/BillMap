import os
from django.db.models.expressions import Value

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models.functions import Concat
from django.views import View

from common.constants import START_CONGRESS, CURRENT_CONGRESS

from home.forms import QueryForm
from bills.models import Bill

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
        return JsonResponse({"bill_list": list(reversed(bills))})
class BillListTitleAPIView(View):
    
    def get(self, request, congressnumber):
        bills_titles=Bill.objects.filter(congress=congressnumber).values_list(
                             'bill_congress_type_number', 'short_title').order_by(
                                 'bill_congress_type_number')
        bill_titles_index = {item[0]:item[1] for item in reversed(bills_titles)}
        return JsonResponse(bill_titles_index)


class GetBillTitleAPIView(View):
    def get(self, request, bill):
        print(bill)
        bill = Bill.objects.filter(bill_congress_type_number=bill).first()
        if not bill:
            return JsonResponse({"status": 404})
        return JsonResponse({'short_title': bill.short_title, 'first_title': bill.titles[0], "status": 200})