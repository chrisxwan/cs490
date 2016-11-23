	


$(document).ready(function() {
	function getJsonFromUrl() {
	  var query = location.search.substr(1);
	  var result = {};
	  query.split("&").forEach(function(part) {
	    var item = part.split("=");
	    result[item[0]] = decodeURIComponent(item[1]);
	  });
	  return result;
	}
	function doPoll() {
		var post_html = 'http://cs490-project.herokuapp.com/check_db?email=' + $("#my-data").attr('data-name');
		dict = getJsonFromUrl();
		$.post(post_html, function(data) {
		    if (data === "1") {
		    	if ('service_acs' in dict) {
		    		var hashed_email = $('#encrypted-email').attr('data-name');
		    		var redirect = 'http://' + dict['service_acs'] + "?hashed_email=" + hashed_email;
		    		location.href = redirect;
		    	} else {
		      		location.href = 'http://cs490-project.herokuapp.com/success';
		      	}
		    }
		    setTimeout(doPoll,1000);
		});
	}

	console.log("here");
	doPoll();
})