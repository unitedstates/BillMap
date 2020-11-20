import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View

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
    return render(request, 'home/home.html', {'form': form})


class BillListAPIView(View):
    
    def get(self, request):
        bills = Bill.objects.values_list('bill_congress_type_number', flat=True)
        return JsonResponse({"bill_list": list(bills)})
