$(document).ready(function() {
   "use strict";

	$(document).on('change', 'input:radio', function(){
	    $('input:radio:checked').not(this).prop('checked', false);
	});
});