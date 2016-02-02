$(document).ready(function() {
	"use strict";

    $("#add-choice").click(function(e) {
        e.preventDefault();
        var count = $('#choices-form-container').children().length;
        var template = $('#choice-template').html();
        var updatedTemplate = template.replace(/__prefix__/g, count);
        $('div#choices-form-container').append(updatedTemplate);
        $('#id_form-TOTAL_FORMS').attr('value', count+1);
    });
});