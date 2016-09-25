$(document).ready(function() {

	$("img").error(function(){
    	$(this).css({ "opacity" : 0 });
  	});

	$("body, html").css({"overflow" : "hidden"});

	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
    	$("head").append('<link href="/static/css/form-mobile.css" rel="stylesheet">');
	}

	$(window).load(function(){
		var width = $("#transportation").width() * .8 - parseInt($("fieldset").css("padding-left")) * 2 + "px";

		$("#bus-route-field").select2({
			width: width
		});

		$(".select2-container").each(function(){
			var right = parseInt($("#apply input").css("padding")) * 2 + "px";
			$(this).siblings("input, select").attr('style', "left: auto !important; right: " + right + " !important;");
		});

		$('#apply').validationEngine('attach', {binded:false});
		
	});

})