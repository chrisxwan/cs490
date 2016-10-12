var loginButton = 0;
var createButton = 0;

$(document).ready(function() {
	

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
	});

	$('#forgot-password').click(function() {
		$("#login-form").attr("action", "/forgot-password");
		$("#login-form").addClass('password-reset');
		$('#login-text').fadeOut(function() {
			$(this).text('Reset Password').fadeIn();
		});
		$("#password-field, #forgot-password").animate({
			height: 0,
			paddingTop: 0,
			paddingBottom: 0,
			border: 0,
			opacity: 0,
			marginBottom: 0,
			marginTop: 0
		}, "slow", function(){
			$(this).remove();
			$("#email-field").focus();
			$('#login-button-actual').attr('value','Reset');
		});

		$(".submit").animate({
			marginTop: "-15px",
			marginBottom: 0
		}, "slow", function(){
			$(this).css({ "margin-top" : "15px" });
		});

		$('.password-reset').ajaxForm({
			beforeSubmit: function(arr, $form, options) {
				$("#email").hide();
				$("#email").val('');
				$(".submit").hide();
				$('.fs-subtitle').remove();
				$('.loading-spinner').fadeIn();
			},
			success: function(html, status, xhr, myForm) {
				$('.loading-spinner').fadeOut("slow", function() {
					if (html['response'] == 1) {
						console.log("here");
						$('<h3 class="fs-subtitle" id="password-status">No application with that email exists!</h3>').insertBefore('#email').show('slow');
						$("#email").fadeIn();
						$("#email").focus();
						$(".submit").fadeIn();
					} else if (html['response'] == 200) {
						$("#email-field").remove();
						$(".submit").remove();
						$('<h3 class="fs-subtitle" id="password-status">An email to reset your password has been sent.</h3>').insertBefore('#email').show('slow');
					} else {
						$('<h3 class="fs-subtitle" id="password-status">Something went wrong... try again or contact us at <a href=mailto:team@yhack.org>team@yhack.org</a></h3>').insertBefore('#email').show('slow');
						$("#email").fadeIn();
						$("#email").focus();
						$(".submit").fadeIn();
					}
				});
			}
		});
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
	});
	$('#password').validationEngine({showOneMessage: true});
	// $('#login-form').validationEngine({showOneMessage: true});
	// $('#create-form').validationEngine({showOneMessage: true});

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