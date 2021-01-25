//TODO add bills_list as a JSON array to the context
var billsDataSample = ['116hr5', '116hr532', '116hr1500', '116hjres31', '116hr1220'];
var billsDataURL = 'bill-list';
$.get(billsDataURL).then(function (results) {
    const billsData = results.bill_list ? results.bill_list.sort() : billsDataSample;
    $("#bill-search").typeahead({
        hint: true,
        minLength: 1,
        highlight: true,
        autoselect: true
    },
    {
        name: 'billsData',
        source: substringMatcher(billsData)
    })
    .on('typeahead:select', function (e, selection) {
        const billUrl = `/bills/${selection}`; 
        console.log(selection);
        console.log(`Setting Go! button href to ${billUrl}`);
        $('#gobutton').attr("href", billUrl);
        window.location = billUrl;
    });
    })
    .catch(function (err) {
        console.log(err);
    });

var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });
        cb(matches);
    };
};

const getSimilarBills = function(e){
    event.preventDefault(e);
    const inputText = document.getElementById("bill-text-textarea").value;
    if(inputText){
    alert(inputText);
    }

}; 

$(document).ready(function() {
});

document.addEventListener('DOMContentLoaded', function() {
    var eventSources = [
        {
            name: 'US Holidays',
            googleCalendarId: 'en.usa#holiday@group.v.calendar.google.com',
            className: 'event-us-holiday'
        },
        {
            // https://www.majorityleader.gov/calendar/ical
            name: 'Majority Leader Events',
            googleCalendarId: '39dfmaqro0ubr9cbr6q6l0sb6ptggfpp@import.calendar.google.com',
            className: 'event-majority-leader'
        },
        {
            // https://www.opm.gov/about-us/open-government/Data/Apps/Holidays/holidays.ical
            name: 'Federal Holidays',
            googleCalendarId: 'fda3ke70gkvd1igbt5p4omtpk6dnng6t@import.calendar.google.com',
            className: 'event-opm'
        }
    ];
    var calendarKeyEl = document.getElementById('calendar-key');

    $.each(eventSources, function(index, eventSource) {
        $(calendarKeyEl)
          .append("<ul><li><div class=\"event-source-color-key " + eventSource.className+ "\"></div>")
          .append(eventSource.name+ "</li></ul>");
    });

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridWeek,dayGridMonth'
        },

        initialView: 'timeGridWeek',
        views: {
            timeGridWeek: {
                dayHeaderContent: (args) => {
                    return moment(args.date).format('ddd D')
                }
            },
            dayGridMonth: {
                dayHeaderContent: (args) => {
                    return moment(args.date).format('ddd D')
                }
            }
        },

        firstDay: 1,
        slotMinTime: '07:00:00',
        slotMaxTime: '20:00:00',

        contentHeight: 'auto',

        displayEventTime: true,

        // THIS KEY WON'T WORK IN PRODUCTION!!!
        // To make your own Google API key, follow the directions here:
        // http://fullcalendar.io/docs/google_calendar/
        googleCalendarApiKey: 'AIzaSyDcnW6WejpTOCffshGDDb4neIrXVUA1EAE',

        eventSources: eventSources,

        eventClick: function(arg) {
            // opens events in a popup window
            window.open(arg.event.url, 'google-calendar-event', 'width=700,height=600');

            arg.jsEvent.preventDefault() // don't navigate in main tab
        }

    });

    calendar.render();
});
