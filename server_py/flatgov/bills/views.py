from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the bills index.")

def bill_view(request, bill):
    context = {'billCongressTypeNumber': bill}
    return render(request, 'bills/bill.html', context)