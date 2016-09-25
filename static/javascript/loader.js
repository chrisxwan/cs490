$(window).load(function(){
	setTimeout(function(){
		$("#blank").fadeOut(750);
	  	$(".loaded").animate({
			opacity: 1
	  	}, 1500, function(){
	  	});
	}, 1100); 
})