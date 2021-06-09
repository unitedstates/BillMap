from events.models import Event, SourceArchive
from dateutil.rrule import *
from common.utils import set_eastern_timezone

import icalendar
import datetime

def process_ical(source):
    print("Processing ical: " + source.name)
    #source.content is not xml

    cal = icalendar.Calendar.from_ical(source.content)

    for vevent in cal.walk('vevent'):
        summary = (vevent.get('summary'),"")[not vevent.get('summary')]
        description = (vevent.get('description'), "")[not vevent.get('description')]
        location = (vevent.get('location'), "")[not vevent.get('location')]

        allDay = True if isinstance(vevent.get('dtstart').dt, datetime.date) else False
        startdate = set_eastern_timezone(vevent.get('dtstart').dt)
        enddate = set_eastern_timezone(vevent.get('dtend').dt)

        eventId = (vevent.get('uid'),"")[not vevent.get('uid')]

        if vevent.get('rrule'):
            reoccur = vevent.get('rrule').to_ical().decode('utf-8')

            print("Recurring event detected, not supported yet")
        else:
            className = "event-opm" if source.name == "OPM Holidays" else "event-house-majority-leader"
            chamber = "house" if source.name == "House Majority Leader" else ""


            existingEvent = False
            try:
                existingEvent = Event.objects.get(sourceName=source.name, eventId=eventId)
            except:
                existingEvent = False

            if existingEvent:
                print("Updating event: " + eventId)
                existingEvent.sourceId=source.id
                existingEvent.title=summary
                existingEvent.description=description
                existingEvent.notes=location
                existingEvent.allDay=allDay
                existingEvent.className=className
                existingEvent.start=startdate
                existingEvent.end=enddate
                existingEvent.chamber=chamber

                existingEvent.save(update_fields=['sourceId',
                                                  'title',
                                                  'description',
                                                  'notes',
                                                  'allDay',
                                                  'className',
                                                  'start',
                                                  'end',
                                                  'chamber'])
            else:
                print("Creating event: " + eventId)
                Event.objects.create(
                    sourceName=source.name,
                    sourceId=source.id,
                    eventId=eventId,
                    title=summary,
                    description=description,
                    notes=location,
                    allDay=allDay,
                    className=className,
                    start=startdate,
                    end=enddate,
                    chamber=chamber)

    print("End processing ical: " + source.name)
    return
