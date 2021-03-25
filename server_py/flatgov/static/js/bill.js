$(document).ready( function () {
    $('#cosponsors-table-top').DataTable({
        sDom: "Rlfrtip",
        bFilter: false,
        bPaginate: false,
        iDisplayLength: 5,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            info: "_START_ to _END_ of _TOTAL_ Cosponsors",
        }
    });
    $('#cosponsors-table').DataTable({
        sDom: "Rlfrtip",
        bFilter: false,
        bPaginate: true,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ Cosponsors",
            lengthMenu: "_MENU_ cosponsors",
        },
        lengthMenu: [100, 30, 5],
    });

    $('#similar-bills-table').DataTable({
        sDom: "Rlfrtip",
        // order: [[ 3, 'desc' ]],
        columnDefs: [
            { "width": "10%", "targets": 0 },
            { "width": "10%", "targets": 1 },
            { "width": "15%", "targets": 2 },
            { "width": "30%", "targets": 3 },
            { "width": "10%", "targets": 4 },
            { "width": "10%", "targets": 5 },
        ],
        bSort: false,
        bFilter: false,
        bPaginate: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            info: "_START_ to _END_ of _TOTAL_ Bills",
            lengthMenu: "_MENU_ bills",
        },
        lengthMenu: [100, 50, 20, 5],
    });

    $('#current-similar-bills-table').DataTable({
        sDom: "Rlfrtip",
        autoWidth: false,
        columnDefs: [
            { "width": "10%", "targets": 0 },
            { "width": "10%", "targets": 1 },
            { "width": "15%", "targets": 2 },
            { "width": "30%", "targets": 3 },
            { "width": "10%", "targets": 4 },
            { "width": "10%", "targets": 5 },
        ],
        bSort: false,
        bFilter: false,
        bPaginate: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            info: "_START_ to _END_ of _TOTAL_ Bills",
        },
    });
    $('#similar-sections-table').DataTable({
        sDom: "Rlfrtip",
        autoWidth: false,
        columnDefs: [
            { "width": "50%", "targets": 0 },
            { "width": "50%", "targets": 1 },
        ],
        bSort: false,
        bFilter: false,
        bPaginate: false,
        iDisplayLength: 30,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ sections",
            lengthMenu: "_MENU_ sections",
        },
        lengthMenu: [100, 30, 5],
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
        $($.fn.dataTable.tables(true)).DataTable()
           .columns.adjust();
     });
});