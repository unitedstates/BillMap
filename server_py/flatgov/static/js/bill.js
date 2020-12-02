$(document).ready( function () {
    $('#related-bills-table').DataTable({
        bFilter: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ Bills",
            lengthMenu: "_MENU_ bills",
        },
        lengthMenu: [5, 10, 20],
    });
    $('#cosponsors-table').DataTable({
        bFilter: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ Cosponsors",
            lengthMenu: "_MENU_ cosponsors",
        },
        lengthMenu: [5, 10, 20],
    });
    $('#similar-bills-table').DataTable({
        bFilter: true,
        language: {
            paginate: {
                "previous": "<",
                "next": ">",
            },
            info: "_START_ to _END_ of _TOTAL_ Bills",
            lengthMenu: "_MENU_ bills",
        },
        lengthMenu: [5, 10, 20],
    });
} );