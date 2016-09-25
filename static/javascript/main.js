var spacing = 1000;
var cookie = false;

function setCookie(value, time) {
  var d = new Date();
  d.setTime(d.getTime() + (time*24*60*60*1000));
  var expires = "expires="+d.toGMTString();
  document.cookie = "c209a57ae54980562bf78bd802b06b97=" + value + "; " + expires;
}

function checkCookie() {
  var name = "c209a57ae54980562bf78bd802b06b97=";
  var arr = document.cookie.split(';');
  for(var i=0; i<arr.length; i++){
    var c = arr[i];
    while (c.charAt(0)==' ') c = c.substring(1,c.length);
    // if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    if (c.indexOf(name) != -1) return true;
  }
  return false;
}

// function to generate a random number range.
function randRange(minNum, maxNum) {
  return (Math.floor(Math.random() * (maxNum - minNum + 1)) + minNum);
}

function logoHeight(screenHeight) {
	if (screenHeight > 700) {
		return "120";
	} else {
		return "80";
	}
}

function logoWidth(screenHeight) {
	if (screenHeight > 700) {
		return "161";
	} else {
		return "107";
	}
}

function logoTop(screenHeight) {
	var tTop = textTop(screenHeight);
	if (screenHeight > 1050) {
		tTop = 300;
	}
	return (screenHeight * 0.57 - tTop) * -1;
}

function textTop(screenHeight) {
	var windowHeight = $(window).height();
	return windowHeight / 2 - 190;
}

$(window).load(function() {
	if (checkCookie()) {
		cookie = true;
	} else {
		setCookie(1, 30);
	}
	if (cookie === true) {
		$('#wrapper').addClass('hidden');
		$('#logo-info').addClass('hidden');
		$('#loading-separate').css('visibility', 'visible');
		$('#inverse').addClass('hidden');
		$('#main').removeClass('hidden');
		$('#logo-cookie').removeClass('hidden');
		$('#bar').raindrops({
			color: '#3E75D9',
			canvasHeight: 140,
			waveLength: 170,
			rippleSpeed: 0.01,
			canvasWidth: 3000,
		});
	}
})

$(document).ready(function() {
	console.log("Thanks for visiting our site! We're looking forward to seeing you at YHack, from November 11-13, 2016!");
	$('#photo-card').click(function() {
		$('#photo-card').css('z-index', '1');
	});
	$('#video-card').click(function() {
		$('#photo-card').css('z-index', '0');
	})


	// Remove background video on mobile devices due to touch issue
	if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
		$('#bottom').addClass('bottom-no-video');
	} else {
		$('#bottom').tubular({videoId: 'MnaA1A495Dc'});
	}

	var screenHeight = $(window).height();
	var screenWidth = $(window).width();
	var marginTop = logoTop(screenHeight);
	var logoH = logoHeight(screenHeight);
	var logoW = logoWidth(screenHeight);
	var wait = 5200;
	if (!checkCookie()) {
		if (screenWidth <= 900 && screenWidth > 700) {
			$('.path')[0].style.animationDuration = "7s";
		} else if (screenWidth <= 700 && screenWidth > 500) {
			$('.path')[0].style.animationDuration = "8.5s";
		} else if (screenWidth <= 500) {
			$('.path')[0].style.animationDuration = "11s";
			wait = 4500;
		}
		window.setTimeout(
			function() {
				$('#loading-image').animate({
						height: logoH,
						width: logoW,
						marginTop: marginTop,
					}, {
						duration: 1000,
						specialEasing: {
							width: "easeInOutExpo",
							height: "easeInOutExpo"
						},
						complete: function() {
							if (screenHeight <= 600) {
								$('#loading-separate').css('bottom', '-100px');
							}
							var textMargin = textTop(screenHeight);
							$('#loading-text').css('margin-top', textMargin);
							$('#loading-text').fadeIn(800);
							$('#loading-separate').css('visibility', 'visible');
							$('#inverse').removeClass('hidden');
							$('#trace').removeClass('hidden');
						}
					});
					window.setTimeout(
						function() {
							$('#inverse').animate({
								bottom: "-=480",
							}, {
								duration: 1000,
								specialEasing: {
									bottom: "easeInOutExpo"
								},
								complete: function() {
									var textMargin = parseInt($('#loading-text').css('margin-top').substring(0,3));
									var textHeight = parseInt($('#loading-text').css('height').substring(0,3));
									$('#loading-buttons').css('margin-top', textMargin + textHeight + 15);
									$('#inverse').addClass('hidden');
									$('#wrapper').addClass('hidden');
									$('#main').removeClass('hidden');
									$('#loading-buttons').fadeIn(400);
									$('#bar').raindrops({
										color: '#3E75D9',
										canvasHeight: 140,
										waveLength: 170,
										rippleSpeed: 0.01,
										canvasWidth: 3000,
									});
								}
							});
						}, wait
					);
			},
			8000
		);
	} 
});

