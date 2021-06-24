from celery import shared_task, current_app
from events.models import Event, SourceArchive
from dateutil.rrule import *
from urllib.request import Request
from .tasks_ical import process_ical
from .tasks_senate_floor import process_xml_senate_floor
from .tasks_senate_committee import process_xml_senate_committee
from .tasks_house_committee import process_html_house_committee

import urllib.request
import datetime

CALENDAR_SOURCES = [{
    "name": "House Majority Leader",
    "url": "https://www.majorityleader.gov/calendar/ical",
    "type": "ical"
}, {
    "name": "OPM Holidays",
    "url": "https://www.opm.gov/about-us/open-government/Data/Apps/Holidays/ical.aspx",
    "type": "ical"
}, {
    "name": "Senate Floor Schedule",
    "url": "https://www.senate.gov/legislative/schedule/floor_schedule.xml",
    "type": "xml_senate_floor"
}, {
    "name": "Senate Committee Schedules",
    "url": "https://www.senate.gov/general/committee_schedules/hearings.xml",
    "type": "xml_senate_committee"
}, {
    "name": "House Committee Schedules",
    "url": "http://docs.house.gov/Committee/Committees.aspx",
    "type": "html_house_committee"
}]

@shared_task(bind=True)
def download_sources(self):

    print("Starting batch job to download calendar sources")
    for source in CALENDAR_SOURCES:
        try:
            download_source(source)
        except Exception as e:
            print("Unknown exception occurred while downloading source: " + source["name"] + " " + str(e))

    return


def download_source(source):

    print("Downloading " + source["name"])

    skip = False
    success = False
    currentSourceArchiveContent = ""

    if source["name"] == "House Floor Schedules":
        now = datetime.datetime.now()
        monday = now - datetime.timedelta(days = now.weekday())
        weekStartDate = monday.strftime("%Y%m%d")
        url = source["url"].format(weekStartDate, weekStartDate)
    else:
        url = source["url"]

    try:
        with urllib.request.urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})) as f:
            currentSourceArchiveContent = f.read().decode('utf-8')

        latestSource = None

        try:
            latestSource = SourceArchive.objects.filter(
                name=source["name"],
                status=SourceArchive.SUCCESS).latest('created')
        except:
            print("No source archive found. This must be a new data source.")

        if currentSourceArchiveContent:
            if latestSource and latestSource.content:
                if latestSource.content == currentSourceArchiveContent:
                    skip = True
                else:
                    success = True
            elif latestSource is None or not latestSource.content:
                success = True

    except Exception as e:
        print("Error " + str(e))


    if skip:
        print("No changes detected from last download. Skipping " + source["name"])
    else:
        currentSourceArchive = SourceArchive.objects.create(
            name=source["name"], url=source["url"], type=source["type"], status=SourceArchive.DOWNLOADING)

        currentSourceArchive.content = currentSourceArchiveContent

        if success:
            currentSourceArchive.status=SourceArchive.SUCCESS
            currentSourceArchive.save(update_fields=['content', 'status'])
        else:
            currentSourceArchive.status=SourceArchive.FAILED
            currentSourceArchive.save(update_fields=['content', 'status'])

        print("Downloaded " + source["name"])

    return

@shared_task(bind=True)
def process_sources(self):

    print("Starting batch job to process calendar sources")
    for source in CALENDAR_SOURCES:
        try:
            process_source(source)
        except Exception as e:
            print("Unknown exception occurred while processing source: " + source["name"] + " " + str(e))

    return

def process_source(source):
    try:
        print("Processing " + source["name"])

        # for each content type found in source download archive, get latest content
        latestSource = SourceArchive.objects.filter(
            name=source["name"],
            status=SourceArchive.SUCCESS).latest('created')

        previousEntryForSource = None
        try:
            previousEntryForSource = Event.objects.filter(sourceName=source["name"]).first()
        except:
            print("No previous entries found. This must be a new source archive.")

        # if source archive is more recent than existing records
        if latestSource:
            process = False

            if previousEntryForSource:
                if latestSource.created > previousEntryForSource.created:
                    # delete all existing entries for source. TODO maybe delete after processing new records
                    # Event.objects.filter(sourceName=source["name"]).delete()
                    # We should consider synchronizing events if we start storing additional metadata in our DB in the future
                    process = True
                else:
                    print("Source is already up-to-date: " + source["name"])
            else:
                process = True

            if process is True:
                # call parser for each content and add events to DB
                if source["type"] == 'ical':
                    process_ical(latestSource)
                elif source["type"] == 'xml_senate_floor':
                    process_xml_senate_floor(latestSource)
                elif source["type"] == 'xml_senate_committee':
                    process_xml_senate_committee(latestSource)
                elif source["type"] == 'html_house_committee':
                    process_html_house_committee(latestSource)
                else:
                    print("Unknown source type: " + source["type"])
        else:
            print("No successful source was found for: " + source["name"])
    except Exception as e:
        print("Exception occurred while processing source: " + source["name"] + " " + str(e))

    print("Processed " + source["name"])
    return
