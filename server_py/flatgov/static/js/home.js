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
        'HAMDT': 'H.Amdt.',
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
            if (substrRegex.test(str.trim().replace(/^\d+/,'')) && !str.match('amdt')) {
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
    $.ajax("https://in-session.house.gov").done(function (response) {
        if (response === "1") {
            $('#session-indicator').append("<i class=\"fa fa-flag\"></i> LIVE");
        }
    });

    var eventSources = [
        {
            name: 'US Holidays',
            label: '* Federal Holidays',
            className: 'event-opm'
        },
        {
            name: 'Senate Floor Events',
            label: '',
            className: 'event-senate-floor'
        },
        {
            name: 'Senate Committee Events',
            label: '',
            className: 'event-senate-committee'
        },
        {
            name: 'House Committee Events',
            label: '',
            className: 'event-house-committee'
        },
        {
            name: 'House Majority Leader',
            label: '',
            className: 'event-house-majority-leader'
        }
    ];
    var calendarKeyEl = document.getElementById('calendar-key');

    $.each(eventSources, function(index, eventSource) {
        $(calendarKeyEl)
          .append("<div style='line-height:16px;' class=\"event-source-color-key p-1 px-3 mx-3 text-white " + eventSource.className+ "\">"+"<div class='d-flex flex-column justify-content-center text-center event-text'>"+"<div>"+eventSource.name+"</div>"+"<small style='line-height:16px; font-size: 10px;'>"+eventSource.label+"</small></div>"+"</div>")
    });

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridWeek,dayGridMonth,timeGridDay'
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

        eventSources: eventSources,

        eventClick: function(arg) {
            // opens events in a popup window
            //window.open(arg.event.url, 'google-calendar-event', 'width=700,height=600');
            window.alert("Open modal");
            arg.jsEvent.preventDefault() // don't navigate in main tab
        },

        events: {
            url: '/events/',
            method: 'GET',
            extraParams: {
                "start-date": '1999-01-01',
                "end-date": '2021-12-31'
            },
            failure: function() {
                alert('There was an error while fetching events!');
            }
        }
    });

    calendar.render();
    $('.fc-today-button').prop("disabled", false);

    $(".fc-button").click(function(event){
        event.preventDefault();
        $('.fc-today-button').removeAttr("disabled");
    });
    
});
