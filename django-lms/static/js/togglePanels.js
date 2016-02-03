$(document).ready(function() {
	"use strict";
	
    $('#show-exams').click(function() {
        $('#exams').toggleClass('hidden');
    });

    $('#show-participants').click(function() {
        $('#participants').toggleClass('hidden');
    });
});