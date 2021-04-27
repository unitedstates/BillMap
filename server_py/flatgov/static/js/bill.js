$(document).ready( function () {
    $('#cosponsors-table-top').DataTable({
        dom: 'Bflrtip',
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
        ordering: false,
        bPaginate: false,
        iDisplayLength: 5,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true
    });

    
    $('#current-similar-bills-table').DataTable({
        dom: "Bflrtip",
        autoWidth: false,
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
            { "width": "10%", "targets": 0 },
            { "width": "10%", "targets": 1 },
            { "width": "15%", "targets": 2 },
            { "width": "30%", "targets": 3 },
            { "width": "10%", "targets": 4 },
            { "width": "10%", "targets": 5 },
        ],
        bSort: false,
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

    $('#similar-bills-table').DataTable({
        dom: "Bflrtip",
        autoWidth: false,
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
            { "width": "10%", "targets": 0 },
            { "width": "10%", "targets": 1 },
            { "width": "15%", "targets": 2 },
            { "width": "30%", "targets": 3 },
            { "width": "10%", "targets": 4 },
            { "width": "10%", "targets": 5 },
        ],
        bSort: false,
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
        autoWidth: false,
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

    $('#cosponsors-table').DataTable({
        dom: 'Bflrtip',
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
        bFilter: true,
        ordering: false,
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

    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
        $($.fn.dataTable.tables(true)).DataTable()
           .columns.adjust();
     });
});