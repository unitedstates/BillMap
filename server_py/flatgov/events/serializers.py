from rest_framework import serializers
from .models import Event, SourceArchive


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['sourceName', 'created', 'updated',
                  'title', 'description', 'notes',
                  'chamber', 'committee', 'subcommittee', 'type',
                  'start', 'end', 'startTime', 'endTime', 'startRecur', 'endRecur', 'allDay', 'className']
