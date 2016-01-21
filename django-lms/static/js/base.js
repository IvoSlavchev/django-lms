function confirmDelete() {
    return confirm("Are you sure?");
}

function searchFilter() {
    var filter = $("#search").val();
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

$("input:not(:checkbox, :radio), textarea, #id_category").addClass('form-control');