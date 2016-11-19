var loginButton = 0;
var createButton = 0;

$(document).ready(function() {

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
	// $('#password').validationEngine({showOneMessage: true});
	// $('#login-form').validationEngine({showOneMessage: true});
	// $('#create-form').validationEngine({showOneMessage: true});
})