from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Event
from .serializers import EventSerializer
from django.db.models import Q

import datetime

def get_events(request):
    startDate = request.GET.get('start')
    endDate = request.GET.get('end')
    start=datetime.date.today()
    end=datetime.date.today()

    chamber =  request.GET.get('chamber')
    committee =  request.GET.get('committee')
    type =  request.GET.get('type')

    if startDate is not None:
        start = datetime.datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S%z')

    if endDate is not None:
        end = datetime.datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%S%z')

    new_end = end + datetime.timedelta(days=1)

    q = Q()

    if start:
        q &= Q(start__gte=start)
    if end:
        q &= Q(end__lte=new_end)
    if chamber and chamber != "all":
        q &= Q(chamber=chamber)
    if committee and committee != "all":
        q &= Q(committee=committee)
    if type and type != "all":
        q &= Q(type=type)

    events = Event.objects.filter(q).order_by('start', 'startTime')

    serializer = EventSerializer(events, many=True)
    return JsonResponse(serializer.data, safe = False)

def get_committees(request):
    committees = Event.objects.order_by('committee').values_list('committee', flat=True).distinct()

    return JsonResponse(list(committees), safe = False)
