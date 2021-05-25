from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Event
from .serializers import EventSerializer

import datetime

def get_events(request):
    startDate = request.GET.get('start-date')
    endDate = request.GET.get('end-date')
    start=datetime.date.today()
    end=datetime.date.today()

    if startDate is not None:
        start = datetime.datetime.strptime(startDate, '%Y-%m-%d')

    if endDate is not None:
        end = datetime.datetime.strptime(endDate, '%Y-%m-%d')

    new_end = end + datetime.timedelta(days=1)

    events = Event.objects.filter(start__range=[start, new_end]).order_by('start', 'startTime')

    serializer = EventSerializer(events, many=True)
    return JsonResponse(serializer.data, safe = False)
