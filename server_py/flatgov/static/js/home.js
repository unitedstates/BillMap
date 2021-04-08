//TODO add bills_list as a JSON array to the context
var billsDataSample = ['116hr5', '116hr532', '116hr1500', '116hjres31', '116hr1220'];
var billsDataURL = 'bill-list';
var allBillData = [];
var currentBillData = [];
var current_year = new Date().getFullYear();
var currentCongress = Math.floor((current_year - 1787) / 2) || 117;
var currentCongressRegex = new RegExp(`^${currentCongress}`);
var selectedBillTitlesData = {};
var getBillsTitles = function(congressnumber) {
    const billsTitlesURL = `bill-titles/${congressnumber}`;
    $.get(billsTitlesURL).then(function (results) {
        selectedBillTitlesData = results;
    });
}
getBillsTitles(currentCongress.toString());

$.get(billsDataURL).then(function (results) {
    allBillData = results.bill_list ? results.bill_list.sort() : billsDataSample;
    currentBillData = allBillData.filter(item => item.match(currentCongressRegex)) 

    $("#bill-search").typeahead({
        hint: true,
        minLength: 1,
        highlight: true,
        autoselect: true
    },
    {
        name: 'currentBillData',
        source: substringMatcher(currentBillData)
    })
    .on('typeahead:select', function (e, selection) {
        const billNumber = billUnFormat(selection);
        const billUrl = `/bills/${billNumber}`; 
        console.log(billNumber);
        console.log(`Setting Go! button href to ${billUrl}`);
        $('#gobutton').attr("href", billUrl);
        window.location = billUrl;
    });
    })
    .catch(function (err) {
        console.log(err);
    });
var stagesFormat = {
        'S': 'S.',
        'HR': 'H.R.',
        'HRES': 'H.Res.',
        'HJRES': 'H.J.Res.',
        'HCONRES': 'H.Con.Res.',
        'SJRES': 'S.J.Res.',
        'SCONRES': 'S.Con.Res.',
        'SRES': 'S.Res.'
    }

// See https://stackoverflow.com/a/39466341/628748
var numstringToOrdinal = function(numstring){

    if (!numstring) {
        return '';
    }

    const n = parseInt(numstring, 10);
    const suffix = [,'st','nd','rd'][n/10%10^1&&n%10]||'th'
    return n.toString() + suffix;
}

var billFormat = function(str) {
    const billCongressTypeNumberRegex = new RegExp(/(?<congress>\d+)(?<type>[a-z]+)(?<billnumber>\d+)/, 'gi');
    const billMatch = billCongressTypeNumberRegex.exec(str);
    const billType = stagesFormat[billMatch.groups.type.toUpperCase()] || '';
    const short_title = selectedBillTitlesData[str] ? ':  ' + selectedBillTitlesData[str] : '';
    return `${billType} ${billMatch.groups.billnumber} (${numstringToOrdinal(billMatch.groups.congress)})${short_title}`
}

// Takes a bill number of the form H.R. 200 (116) and returns 116hr200
var billUnFormat = function(str) {
    const parensCongressRegex = new RegExp(/\((?<congress>\d+)[thstrd]*\)/, '');
    const congressMatch = parensCongressRegex.exec(str)
    return congressMatch.groups.congress + str.replace(/[\. ]/gi, '').replace(/\(.*$/, '').toLowerCase()
}

var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q.replace(/[\s\.]/g, '').toLowerCase().trim(), 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
            if (substrRegex.test(str.trim().replace(/^\d+/,''))) {
                matches.push(billFormat(str));
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
    $('#selectcongress').change(function() {
        const $option = $(this).find('option:selected');
        const value = $option.val(); //returns the value of the selected option.
        const text = $option.text(); //returns the text of the selected option.
        console.log(`Selected Congress: ${value}`)
        if (value == 'all'){
            currentBillData = [...allBillData]
        }else{
            getBillsTitles(value);
            const congressRegex = new RegExp(`^${value}`);
            currentBillData = allBillData.filter(item => item.match(congressRegex)) 
        }
        //console.log(currentBillData);
        $("#bill-search").typeahead('destroy');
        $("#bill-search").typeahead({
            hint: true,
            minLength: 1,
            highlight: true,
            autoselect: true
        },
        {
            name: 'currentBillData',
            source: substringMatcher(currentBillData)
        })
        .on('typeahead:select', function (e, selection) {
            const billNumber = billUnFormat(selection);
            const billUrl = `/bills/${billNumber}`; 
            console.log(billNumber);
            console.log(`Setting Go! button href to ${billUrl}`);
            $('#gobutton').attr("href", billUrl);
            window.location = billUrl;
        });
        
    });
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
