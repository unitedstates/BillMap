$(document).ready( function () {

    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
        $($.fn.dataTable.tables(true)).DataTable()
          .columns.adjust();
    });

    $('#cosponsors-table-top').DataTable({
        dom: 'flrtBip',
        buttons: [
            {
                extend: 'copy',
                text: 'Copy to clipboard'
            },
            {
                extend: 'csv',
                text: 'Export to CSV'
            },
            'excelHtml5'
        ],
        bFilter: false,
        bSort: true,
        aaSorting: [],
        ordering: true,
        bPaginate: false,
        iDisplayLength: 5,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true
    });

    
    $('#current-similar-bills-table').DataTable({
        dom: "flrtBip",
        autoWidth: true,
        buttons: [
            {
                extend: 'copy',
                text: 'Copy to clipboard',
            },
            
            {
                extend: 'csv',
                text: 'Export to CSV'
            },
            'excelHtml5'
        ],
        columnDefs: [
            { "width": "15%", "targets": 0 },
            { "width": "35%", "targets": 1 },
            { "width": "35%", "targets": 2 },
            { "width": "15%", "targets": 3 },
        ],
        bSort: true,
        aaSorting: [],
        ordering: true,
        bFilter: true,
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ Bills",
        },
    })

    $('#similar-bills-table').DataTable({
        dom: "flrtBip",
        autoWidth: true,
        buttons: [
            {
                extend: 'copy',
                text: 'Copy to clipboard',
            },
            
            {
                extend: 'csv',
                text: 'Export to CSV',
                bottom: true
            },
            'excelHtml5'
        ],
        columnDefs: [
            { "width": "15%", "targets": 0 },
            { "width": "35%", "targets": 1 },
            { "width": "35%", "targets": 2 },
            { "width": "15%", "targets": 3 },
        ],
        bSort: false,
        aaSorting: [],
        ordering: true,
        bFilter: true,
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            info: "_START_ to _END_ of _TOTAL_ Bills",
        },
    })

    $('#similar-sections-table').DataTable({
        dom: "Rlfrtip",
        autoWidth: true,
        buttons: [
            {
                extend: 'copy',
                text: 'Copy to clipboard',
            },
            
            {
                extend: 'csv',
                text: 'Export to CSV'
            },
            'excelHtml5'
        ],
        columnDefs: [
            { "width": "50%", "targets": 0 },
            { "width": "50%", "targets": 1 },
        ],
        bSort: false,
        aaSorting: [],
        ordering: true,
        bFilter: true,
        bPaginate: false,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ sections"
        },
    });

    var cosponsorTable = $('#this-congress-cosponsors-table').DataTable({
        dom: 'flrtBip',
        buttons: [
            {
                extend: 'copy',
                text: 'Copy to clipboard',

            },
            {
                extend: 'csv',
                text: 'Export to CSV'
            },
            'excelHtml5'
        ],
        bFilter: true,
        ordering: true,
        aaSorting: [],
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ cosponsors"
        },
    });

    var cosponsorTable = $('#all-congress-cosponsors-table').DataTable({
        dom: 'flrtBip',
        buttons: [
            {
                extend: 'copy',
                text: 'Copy to clipboard',

            },
            {
                extend: 'csv',
                text: 'Export to CSV'
            },
            'excelHtml5'
        ],
        bFilter: true,
        ordering: true,
        aaSorting: [],
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ cosponsors"
        },
    });

    $('#crs-reports-table').DataTable({
        dom: 'flrtip',
        bFilter: true,
        ordering: true,
        aaSorting: [],
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            emptyTable: "No relevant CRS reports are available",
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ reports"
        },
    });

    $('#statements-of-table').DataTable({
        dom: 'flrtip',
        bFilter: true,
        ordering: true,
        aaSorting: [],
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            emptyTable: "No relevant statements are available",
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ statements"
        },
    });

    $('#cbo-scores-table').DataTable({
        order: [[2, 'asc']],
        dom: 'flrtip',
        bFilter: true,
        ordering: true,
        aaSorting: [],
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            emptyTable: "No relevant CBO scores are available",
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ CBO scores"
        },
    });

    $('#relevant-committee-documents-table').DataTable({
        order: [[4, 'desc']],
        dom: 'flrtip',
        bFilter: true,
        ordering: true,
        aaSorting: [],
        bPaginate: true,
        bLengthChange: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            emptyTable: "No relevant committee documents are available",
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ committee documents"
        },
    });

    cosponsorTable.buttons().container()
    .appendTo('#unique-test');

});
