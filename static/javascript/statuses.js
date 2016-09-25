$(document).ready(function(){

	$("img").error(function(){
    	$(this).css({ "opacity" : 0 });
  	});

	(function foo () {
		$("#content").css({ "background-position" : "" });
		$('#content').animate({
		  'background-position-x': '300px'
		}, 500, "linear", function(){
			foo();
		});
	})();

	var sendingInProgress = false;
	$('#resend-email').click(function (event){
		event.preventDefault();
		sendingInProgress = true;
	    $.get( $(this).attr('href'), function( data ) {
	    	$('h3').remove();
	    	$("#content").append('<h3 id="sent-message">' + data['message'] + '</h3>');
	    	sendingInProgress = false;
		});
	    return false; //for good measure
	});
});
