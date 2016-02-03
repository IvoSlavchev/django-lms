"use strict";

function searchFilter() {
    var filter = $('#search').val();
    $(':checkbox').each(function() {
        if ($(this).parent().text().indexOf(filter) == 1 || !filter) {
            $(this).show();
            $(this).parent().show();
        } else {
            $(this).hide();
            $(this).parent().hide();
        }
    });
}