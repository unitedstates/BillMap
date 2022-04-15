import datetime
import xmltodict

from common.utils import set_eastern_timezone
from events.models import Event


def process_xml_senate_floor(source):
    print("Processing xml senate floor data: " + source.name)
    data = xmltodict.parse(source.content)

    meetingsBag = data["meetings"]
    meetingBag = meetingsBag["meeting"]
    year = meetingsBag["year"]
    congress = meetingsBag["congress"]
    session = meetingsBag["session"]

    # No event IDs, delete events that are in current year before starting since floor xml has events for current year
    starting_day_of_current_year = set_eastern_timezone(datetime.datetime.now().date()).replace(
        month=1, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    Event.objects.filter(sourceName=source.name, start__gte=starting_day_of_current_year).delete()

    for meeting in meetingBag:
        conveneElement = meeting["convene"]
        conveneBusiness = conveneElement["@business"]  # optional, "", R, R2
        conveneMeasure = conveneElement["@measure"]  # optional, "", s937
        conveneMonth = conveneElement["@month"]  # 04
        conveneDate = conveneElement["@date"]  # 19
        conveneTime = conveneElement["@time"]  # 1500

        conveneTitle = source.name if not conveneElement["@title"] else conveneElement["@title"]

        if "full_text" in conveneElement and conveneElement["full_text"] is not None:
            if "#text" in conveneElement["full_text"]:
                conveneFullText = conveneElement["full_text"]["#text"]
            else:
                conveneFullText = conveneElement["full_text"]
        else:
            conveneFullText = "This information is not available yet."

        #measure
        # <convene business="" date="1" day="F" measure="" month="01" time="1200" title="" year="">
        #    <full_text>12:00 p.m.: Convene and resume consideration of the veto message on <measure>h6395</measure>,
        #    the National Defense Authorization Act for Fiscal Year 2021.</full_text>
        #</convene>

        adjournElement = meeting["adjourn"]
        adjournTime = (adjournElement["@time"], "")[not adjournElement["@time"]].replace(":", "")  # optional, "", 1812
        adjournVotes = adjournElement["@votes"]  # optional, "", 182, 182-183

        if "full_text" in adjournElement and adjournElement["full_text"] is not None:
            if "#text" in adjournElement["full_text"]:
                adjournFullText = adjournElement["full_text"]["#text"]
            else:
                adjournFullText = adjournElement["full_text"]
        else:
            adjournFullText = "This information is not available yet."

        description = "{} Congress {} Session {} - Convene Notes=[{}] Adjourn Notes=[{}]".format(
            year, congress, session, conveneFullText, adjournFullText
        )

        if not adjournTime:
            adjournTime = str(int(conveneTime) + 100)

        start = set_eastern_timezone(datetime.datetime.strptime("{} {} {} {}".format(
            conveneMonth, conveneDate, year, conveneTime
        ), "%m %d %Y %H%M"))
        end = set_eastern_timezone(datetime.datetime.strptime("{} {} {} {}".format(
            conveneMonth, conveneDate, year, adjournTime
        ), "%m %d %Y %H%M"))

        Event.objects.create(
            sourceName=source.name,
            sourceId=source.id,
            title=conveneTitle,
            description=description,
            notes=conveneMeasure,
            chamber="senate",
            className="event-senate-floor",
            start=start,
            end=end,
            allDay=False
        )

    print("End processing xml senate floor data: " + source.name)
    return
