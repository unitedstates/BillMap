from events.models import Event, SourceArchive
from dateutil.rrule import *
from urllib.request import Request
from email.utils import parsedate
from time import mktime
from common.utils import set_eastern_timezone

import urllib.request
import re
import lxml.etree
import datetime

def process_html_house_committee(source):
    print("Processing html house committee schedule data: " + source.name)

    # go through each committee option
    for cmteCode in re.findall(r'<option value="(....)">', source.content):

        # Download the feed for this committee.
        print("Fetching events for committee " + cmteCode)
        html = ""

        with urllib.request.urlopen(Request("http://docs.house.gov/Committee/RSS.ashx?Code={}".format(cmteCode),
                                            headers={'User-Agent': 'Mozilla/5.0'})) as f:
            html = f.read().decode('utf-8')

        # It's not really valid?
        html = html.replace("&nbsp;", " ")

        # Parse and loop through the meetings listed in the committee feed.
        dom = lxml.etree.fromstring(html)

        processed_meetings = [] # keep track of processed meetings to prevent duplicates

        # original start to loop
        for meetingItem in dom.xpath("channel/item"):
            pubDate = datetime.datetime.fromtimestamp(mktime(parsedate(meetingItem.xpath("string(pubDate)"))))

            # skip old records of meetings, some of which just give error pages
            if pubDate < (datetime.datetime.now() - datetime.timedelta(days=10)):
                continue

            eventurl = meetingItem.xpath("link")[0].text
            event_id = re.search(r"EventID=(\d+)$", eventurl)
            if not event_id: continue # weird empty event showed up
            event_id = event_id.group(1)
            if event_id in processed_meetings:
                continue
            else:
                processed_meetings.append(event_id)
                xmlUrl = meetingItem.xpath("enclosure")[0].get("url")
                if xmlUrl:
                    process_xml_house_committee_event(source, xmlUrl, event_id)
                else:
                    print("Skipping meeting item that does not have enclosure URL")

    print("End processing html house committee schedule data: " + source.name)
    return

def process_xml_house_committee_event(source, xmlUrl, event_id):
    try:
        with urllib.request.urlopen(Request(xmlUrl,
                                            headers={'User-Agent': 'Mozilla/5.0'})) as f:
            xml = f.read().decode('utf-8')

        dom = lxml.etree.fromstring(xml)

        try:
            congress = int(dom.xpath("//@congress-num")[0])
            occurs_at = dom.xpath("string(meeting-details/meeting-date/calendar-date)") + " " + dom.xpath("string(meeting-details/meeting-date/start-time)")
            start = set_eastern_timezone(datetime.datetime.strptime(occurs_at, "%Y-%m-%d %H:%M:%S"))

            end = start + datetime.timedelta(hours=1)
        except Exception as e:
            raise ValueError("Invalid meeting data (probably server error) in %s." % event_id + " " + str(e))

        current_status = str(dom.xpath("string(current-status)"))
        if current_status not in ("S", "R"):
            # If status is "P" (postponed and not yet rescheduled) or "C" (cancelled),
            # don't include in output.
            return

        topic = dom.xpath("string(meeting-details/meeting-title)")

        committee_names = []
        for com in dom.xpath("meeting-details/committees"):
            comte = com.xpath("string(committee-name)")
            if comte != None:
                committee_names.append(com.xpath("string(committee-name)"))
        for scom in dom.xpath("meeting-details/subcommittees"):
            scomte = scom.xpath("string(committee-name)")
            if scomte != None:
                committee_names.append(scom.xpath("string(committee-name)"))

        room = None
        for n in dom.xpath("meeting-details/meeting-location/capitol-complex"):
            room = n.xpath("string(building)") + " " + n.xpath("string(room)")

        bills = []
        for bill_id in dom.xpath("meeting-documents/meeting-document[@type='BR']/legis-num"):
            # validating bill ids
            bill_id = house_bill_id_formatter(bill_id.text, congress)
            if bill_id != None:
                bills.append(bill_id)

        try:
            notes = dom.xpath("meeting-details/notes")[0].text
        except:
            notes = ""

        try:
            meeting_type = dom.xpath("//@meeting-type")[0] # HHRG, HMKP
        except:
            meeting_type = ""

        type = ""
        if meeting_type is "HHRG":
            type = "hearing"
        elif meeting_type is "HMKP":
            type = "markup"
        elif re.search("hearing", notes, flags=re.IGNORECASE):
            type = "hearing"
        else:
            type = "markup"

        # Repeat the event for each listed committee or subcommittee, since our
        # data model supports only a single committee/subcommittee ID per event.

        orgs = []
        for c in dom.xpath("meeting-details/committees/committee-name"):
            sc_exists = False
            for sc in dom.xpath("meeting-details/subcommittees/committee-name"):
                sc_exists = True
                Event.objects.create(
                    sourceName=source.name,
                    title=topic,
                    description="{} Congress meeting in {} to discuss {} {}".format(congress, room, topic, bills),
                    notes=notes,
                    chamber="house",
                    className="event-house-committee",
                    committee=c.text,
                    committeeCode=c.get("id"),
                    subcommittee=sc.text,
                    start=start,
                    end=end,
                    type = type,
                    url = xmlUrl,
                    allDay=False)

            if not sc_exists:
                Event.objects.create(
                    sourceName=source.name,
                    title=topic,
                    description="{} Congress meeting in {} to discuss {} {}".format(congress, room, topic, bills),
                    notes=notes,
                    chamber="house",
                    className="event-house-committee",
                    committee=c.text,
                    committeeCode=c.get("id"),
                    start=start,
                    end=end,
                    type = type,
                    url = xmlUrl,
                    allDay=False)

    except Exception as e:
        print("Error parsing " + xmlUrl + " " + str(e))
    return

def house_bill_id_formatter(bill_id, congress):
    # make sure there is a number
    if bill_id == None or bill_id == '':
        return None
    else:
        bill_id = bill_id.strip()
        digit = False
        alpha = False
        for char in bill_id:
            if char.isdigit():
                digit = True
            if char.isalpha():
                alpha = True

        if digit == False:
            return None
        # look for missing hr, though this risks mislabeling continuing and joint resolutions
        if alpha == False:
            bill_id = "hr" + bill_id
        else:
            bill_id = bill_id.replace(".", "").replace(" ", "").lower()

        bill_id = bill_id + "-" + str(congress)
        return bill_id
