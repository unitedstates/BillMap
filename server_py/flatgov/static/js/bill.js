$(document).ready( function () {
    $('#related-bills-table').DataTable({
        sDom: "Rlfrtip",
        bFilter: true,
        iDisplayLength: 100,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ Bills",
            lengthMenu: "_MENU_ bills",
        },
        lengthMenu: [100, 50, 20, 5],
    });
    $('#cosponsors-table').DataTable({
        sDom: "Rlfrtip",
        bFilter: true,
        iDisplayLength: 100,
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
        lengthMenu: [100, 50, 20, 5],
    });
    $('#similar-bills-table').DataTable({
        sDom: "Rlfrtip",
        bFilter: true,
        iDisplayLength: 100,
        scrollY: '50vh',
        scrollX: true,
        scrollCollapse: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ Bills",
            lengthMenu: "_MENU_ bills",
        },
        lengthMenu: [100, 50, 20, 5],
        order: [[ 2, 'desc' ]]
    });
} );