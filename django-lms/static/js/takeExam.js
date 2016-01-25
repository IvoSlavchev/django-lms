$(document).ready(function() {		

	function lockExam() {	
		var input = prompt("Enter exam password:");
		if (input == password) {
			setCookie('password', input);
			return $(".hidden").removeClass("hidden");
		}
		history.go(-1);
	}

	function setCookie(name, value) {
		document.cookie = name + '=' + value;
	}

	function getCookie(name) {
		var re = new RegExp(name + "=([^;]+)");
	    var value = re.exec(document.cookie);
	    return (value != null) ? unescape(value[1]) : null;
	}

	function clearCookie(name) {
		document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
	}

	function rebuildTime(time) {
		var hr = Math.floor(time / 3600);
		var min = Math.floor(time / 60);
		var sec = time - min * 60;	
		var rem = (hr > 9 ? hr : "0" + hr) + ":" + (min > 9 ? min : "0" + min) + ":" + (sec > 9 ? sec : "0" + sec);
		if (time <= 60) {
			$("#remaining").css('color', 'red');
		}
		$("#remaining").text("Remaining time: " + rem);
	}

	var cached_pwd = getCookie('password');
	if (password && cached_pwd == null) {	
		lockExam();
	} else {
		$(".hidden").removeClass("hidden");
	}

	var limit = raw_limit.split(":");
	var seconds = getCookie('time_limit') || limit[0] * 3600 + limit[1] * 60;
	var counter = setInterval(timer, 1000);
	rebuildTime(seconds);

	function timer() {
		seconds -= 1;
		if (seconds == 0) {
			clearInterval(counter);
	    	$("#submit").click();
	 	}
	 	rebuildTime(seconds);
	 	setCookie('time_limit', seconds);
	}

	$("a").click(function(e) {
		if (confirm("Exam in progress. Choosing to continue will submit your current answers.")) {		
			$("#submit").click();
		}
		return false;
	});

	$("#submit").click(function() {
		clearCookie('time_limit');
		clearCookie('password');
	});
});