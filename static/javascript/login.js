$(document).ready(function(){
	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
		$("head").append('<link href="static/css/form-mobile.css" rel="stylesheet">');
		$("#login-wrapper").css({
			"margin-top": "-300px"
		});
	}
	$('#login').validationEngine('attach', {binded:false});

	$('#reset-password').click(function() {
		$('.fs-error').remove();
		$("#login").addClass('password-reset');
		$("#login").attr("action", "/forgot-password");

		$("#password-field, #login-application-redirect, #reset-password").animate({
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
		});

		$(".submit").animate({
			marginTop: "-10px",
			marginBottom: 0
		}, "slow", function(){
			$(this).css({ "margin-top" : "10px" });
		})

		$("#login-title").fadeOut("slow", function() {
			$(this).html("Reset Password");
		}).fadeIn("slow");

		$('.password-reset').ajaxForm({
			beforeSubmit: function(arr, $form, options) {
				$("#email-field").hide();
				$("#email-field").val('');
				$(".submit").hide();
				$('.fs-subtitle').remove();
				$('.loading-spinner').fadeIn();
			},
			success: function(html, status, xhr, myForm) {
				$('.loading-spinner').fadeOut("slow", function() {
					if (html['response'] == 1) {
						$('<h3 class="fs-subtitle" id="password-status">No application with that email exists. Try again!</h3>').insertAfter('#login-title').show('slow');
						$("#email-field").fadeIn();
						$("#email-field").focus();
						$(".submit").fadeIn();
					} else if (html['response'] == 200) {
						$("#email-field").remove();
						$(".submit").remove();
						$('<h3 class="fs-subtitle" id="password-status">An email to reset your password has been sent.  Please contact <a href=mailto:team@yhack.org>team@yhack.org</a> with any questions.</h3>').insertAfter('#login-title').show('slow');
					} else {
						$('<h3 class="fs-subtitle" id="password-status">Something went wrong... try again or contact us at <a href=mailto:team@yhack.org>team@yhack.org</a></h3>').insertAfter('#login-title').show('slow');
						$("#email-field").fadeIn();
						$("#email-field").focus();
						$(".submit").fadeIn();
					}
				});
			}
		});
	});


	

})