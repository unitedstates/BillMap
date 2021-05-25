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

        if vevent.get('rrule'):
            reoccur = vevent.get('rrule').to_ical().decode('utf-8')

            print("Recurring event detected, not supported yet")
        else:
            className = "event-opm" if source.name == "OPM Holidays" else "event-house-majority-leader"

            Event.objects.create(
                sourceName=source.name,
                title=summary,
                description=description,
                notes=location,
                allDay=allDay,
                className=className,
                start=startdate,
                end=enddate)

    print("End processing ical: " + source.name)
    return
