$("ul label").each(function(i) {
    $(this).addClass('label');
    $(this).append(emails[i]);
});