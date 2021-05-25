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
        committeeCode = meeting["cmte_code"] #SSFR00
        committee = meeting["committee"] # Foreign Relations
        dayOfWeek = meeting["day_of_week"] # Wednesday
        room = meeting["room"] # SD-106
        matter = meeting["matter"] # text

        start = set_eastern_timezone(parse_date_from_string(meeting["date"]))
        end = start + datetime.timedelta(hours=1)

        if "sub_cmte" in meeting and meeting["sub_cmte"] is not None:
            subCommittee = meeting["sub_cmte"] # optional, Labor, Health and Human Services, and Education, and Related Agencies
        else:
            subCommittee = None

        title = committee if not subCommittee else "{} - {}".format(committee, subCommittee)
        description = "{} {} in Room {} - {}".format(meeting["date"], dayOfWeek, room, matter)

        isHearing = True if re.search("hearing", matter, flags=re.IGNORECASE) else False

        Event.objects.create(
            sourceName=source.name,
            title=title,
            description=description,
            notes=room,
            className="event-senate-committee-hearing" if isHearing else "event-senate-committee-markup",
            start=start,
            end=end,
            chamber="senate",
            committee=committee,
            committeeCode = committeeCode,
            subcommittee=subCommittee,
            type="hearing" if isHearing else "markup",
            allDay=False)

    print("End processing xml senate committee schedule data: " + source.name)
    return
