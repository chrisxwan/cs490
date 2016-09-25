$(document).ready(function(){
	$("#decline").bind("click", function(e){
		$("#confirm-view").animate({
			opacity: 0
		}, "fast", function(){
			$("#confirm-view").hide();
			$("#decline-view").show();
			$("#decline-view").animate({
				opacity: 1
			}, "fast");
		});
	})

	$("#back-decline-button").bind("click", function(e){
		$("#decline-view").animate({
			opacity: 0
		}, "fast", function(){
			$("#decline-view").hide();
			$("#confirm-view").show();
			$("#confirm-view").animate({
				opacity: 1
			}, "fast");
		});
	})
})