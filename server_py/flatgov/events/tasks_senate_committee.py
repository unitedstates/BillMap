from events.models import Event, SourceArchive
from dateutil.rrule import *
from common.utils import set_eastern_timezone

import xmltodict
import re
import datetime

def parse_date_from_string(str_date):
    for fmt in ("%d-%b-%Y %I:%M %p", '%d-%b-%Y'):
        try:
            return datetime.datetime.strptime(str_date, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found for ' + str_date)

def process_xml_senate_committee(source):
    print("Processing xml senate committee schedule data: " + source.name)
    data = xmltodict.parse(source.content)

    cssMeetingsScheduledBag = data["css_meetings_scheduled"]
    meetingBag = cssMeetingsScheduledBag["meeting"]

    for meeting in meetingBag:
        eventId = meeting["identifier"] if "identifier" in meeting else "" # 329690
        committeeCode = meeting["cmte_code"] # SSFR00
        committee = meeting["committee"] # Foreign Relations
        dayOfWeek = meeting["day_of_week"] # Wednesday
        room = meeting["room"] # SD-106
        matter = meeting["matter"] # text

        start = set_eastern_timezone(parse_date_from_string(meeting["date"]))
        end = start + datetime.timedelta(hours=1)

        hasSubCommittee = False
        hasMultipleSubCommittees = False

        if "sub_cmte" in meeting and meeting["sub_cmte"] is not None:
            hasSubCommittee = True
            subCommittee = meeting["sub_cmte"] # optional, Labor, Health and Human Services, and Education, and Related Agencies

            if isinstance(subCommittee, list):
                hasMultipleSubCommittees = True
        else:
            subCommittee = None

        title = committee if not subCommittee else "{} - {}".format(committee, subCommittee)
        description = "{} {} in Room {} - {}".format(meeting["date"], dayOfWeek, room, matter)

        isHearing = True if re.search("hearing", matter, flags=re.IGNORECASE) else False


        existingEvent = False

        if hasMultipleSubCommittees:
            for sc in subCommittee:
                try:
                    existingEvent = Event.objects.get(sourceName=source.name, subCommittee=sc, eventId=eventId)
                except:
                    existingEvent = False

                if existingEvent:
                    print("Updating event: " + eventId)
                    existingEvent.sourceId=source.id
                    existingEvent.title=title
                    existingEvent.description=description
                    existingEvent.notes=room
                    existingEvent.allDay=False
                    existingEvent.className="event-senate-committee" if isHearing else "event-senate-committee"
                    existingEvent.start=start
                    existingEvent.end=end
                    existingEvent.type="hearing" if isHearing else "markup"
                    existingEvent.chamber="senate"
                    existingEvent.committee=committee
                    existingEvent.committeeCode=committeeCode
                    existingEvent.subcommittee=sc

                    existingEvent.save(update_fields=['sourceId',
                                                      'title',
                                                      'description',
                                                      'notes',
                                                      'allDay',
                                                      'className',
                                                      'start',
                                                      'end',
                                                      'type',
                                                      'chamber',
                                                      'committee',
                                                      'committeeCode',
                                                      'subCommittee'])
                else:
                    print("Creating event: " + eventId)
                    Event.objects.create(
                        sourceName=source.name,
                        sourceId = source.id,
                        eventId = eventId,
                        title=title,
                        description=description,
                        notes=room,
                        className="event-senate-committee" if isHearing else "event-senate-committee",
                        start=start,
                        end=end,
                        chamber="senate",
                        committee=committee,
                        committeeCode =committeeCode,
                        subcommittee=sc,
                        type="hearing" if isHearing else "markup",
                        allDay=False)
        else:
            try:
                existingEvent = Event.objects.get(sourceName=source.name, eventId=eventId)
            except:
                existingEvent = False

            if existingEvent:
                print("Updating event: " + eventId)
                existingEvent.sourceId=source.id
                existingEvent.title=title
                existingEvent.description=description
                existingEvent.notes=room
                existingEvent.allDay=False
                existingEvent.className="event-senate-committee" if isHearing else "event-senate-committee"
                existingEvent.start=start
                existingEvent.end=end
                existingEvent.type="hearing" if isHearing else "markup"
                existingEvent.chamber="senate"
                existingEvent.committee=committee
                existingEvent.committeeCode=committeeCode
                existingEvent.subcommittee=subCommittee if subCommittee else ""

                existingEvent.save(update_fields=['sourceId',
                                                  'title',
                                                  'description',
                                                  'notes',
                                                  'allDay',
                                                  'className',
                                                  'start',
                                                  'end',
                                                  'type',
                                                  'chamber',
                                                  'committee',
                                                  'committeeCode',
                                                  'subCommittee'])
            else:
                print("Creating event: " + eventId)
                Event.objects.create(
                    sourceName=source.name,
                    sourceId = source.id,
                    eventId = eventId,
                    title=title,
                    description=description,
                    notes=room,
                    className="event-senate-committee" if isHearing else "event-senate-committee",
                    start=start,
                    end=end,
                    chamber="senate",
                    committee=committee,
                    committeeCode =committeeCode,
                    subcommittee=subCommittee if subCommittee else "",
                    type="hearing" if isHearing else "markup",
                    allDay=False)

    print("End processing xml senate committee schedule data: " + source.name)
    return
