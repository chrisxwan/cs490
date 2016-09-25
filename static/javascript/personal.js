var loginButton = 0;
var createButton = 0;

$(document).ready(function() {
	console.log("here");

	$('#login-button').on('click', function() {
		if (createButton === 1) {
			$('#create-form').animate({
				opacity: 0.0
			}, 400, function() {
				showLogin();
				$('#create-form').hide(500, function() {
					createButton = 0;
					$('#create-button').animate({
						opacity: 1.0
					}, 400);
				});
			});
		} else {
			showLogin();
		}
	})

	$('#create-button').on('click', function() {
		if (loginButton === 1) {
			$('#login-form').animate({
				opacity: 0.0
			}, 400, function() {
				showCreate();
				$('#login-form').hide(400, function() {
					loginButton = 0;
					$('#login-button').animate({
						opacity: 1.0
					}, 400);
				});
			});
		} else {
			showCreate();
		}
	})

	function showCreate() {
		$('#create-button').animate({
			opacity: 0.0,
		}, 400, function() {
			createButton = 1;
			// $('#loggin-button').css('display', 'none');
			$('#create-form').css('opacity', '0.0');
			$('#create-form').show(500, function() {
				$('#create-form').animate({
					opacity: 1.0
				}, 400);
			});
			// $('#login-form').css('visibility', 'visible');
			// $('#login-form').fadeIn(500);
		})
	}

	function showLogin() {
		$('#login-button').animate({
			opacity: 0.0,
		}, 400, function() {
			loginButton = 1;
			// $('#loggin-button').css('display', 'none');
			$('#login-form').css('opacity', '0.0');
			$('#login-form').show(400, function() {
				$('#login-form').animate({
					opacity: 1.0
				}, 400);
			});
			// $('#login-form').css('visibility', 'visible');
			// $('#login-form').fadeIn(500);
		})
	}
})