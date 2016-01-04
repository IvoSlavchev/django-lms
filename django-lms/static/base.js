function confirmDelete() {
    return confirm("Are you sure?");
}

function searchFilter() {
    var filter = $("#id_search").val();
    $(':checkbox').each(function() {
        if ($(this).parent().text().indexOf(filter) != -1) {
            $(this).show();
            $(this).parent().show();
        } else {
            $(this).hide();
            $(this).parent().hide();
        }
    });
}