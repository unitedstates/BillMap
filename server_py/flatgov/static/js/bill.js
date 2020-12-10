$(document).ready( function () {
    $('#related-bills-table').DataTable({
        bFilter: true,
        iDisplayLength: 100,
        scrollY: '50vh',
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
        bFilter: true,
        iDisplayLength: 100,
        scrollY: '50vh',
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
        bFilter: true,
        iDisplayLength: 100,
        scrollY: '50vh',
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