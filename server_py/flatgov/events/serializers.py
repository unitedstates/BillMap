from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['sourceName', 'sourceId', 'eventId', 'created',
                  'updated', 'referenceUrl', 'title', 'description',
                  'notes', 'chamber', 'committee', 'subcommittee', 'type',
                  'start', 'end', 'startTime', 'endTime', 'startRecur',
                  'endRecur', 'allDay', 'className']
