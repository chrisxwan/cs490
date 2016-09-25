$(window).load(function(){
	$("body, html").css({"overflow" : "hidden"});
	setTimeout(function(){
		$("#blank").fadeOut(750);
	  	$(".loaded").animate({
			opacity: 1
	  	}, 1500, function(){
	  		function backgroundOverflow() {
				var windowHeight = $(window).height();
				if (windowHeight <= 775) {
					$("body, html").css({"overflow" : "visible"});
				} else {
					$("body, html").css({"overflow" : "hidden"});
				}
			}
			backgroundOverflow();
			$(window).bind('resize', backgroundOverflow);
	  	});
	}, 1100); 
})