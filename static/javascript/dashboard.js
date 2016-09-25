$(document).ready(function(){

	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
    	$("head").append('<link href="/static/css/dashboard-mobile.css" rel="stylesheet"><link href="/static/css/button-mobile.css" rel="stylesheet">');
	}
	$("#logo-home").click(function(){
		document.location.href="/";
	});

	$(window).load(function(){
		$(".loaded").animate({
			"opacity" : 1
		}, "slow");
	});
})