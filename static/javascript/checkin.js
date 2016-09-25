$(document).ready(function(){
	$('#checkin').ajaxForm({
		beforeSubmit: function(arr, $form, options) {
			$('.fs-error').remove();
			$("#email-field").hide();
			$(".submit").hide();
			$('.loading-spinner').fadeIn();
		},
		success: function(html, status, xhr, myForm) {
			$('.loading-spinner').fadeOut("slow", function() {
				$('.fs-error').fadeIn();
				if (html['status'] == 0) {
					$('<h3 class="fs-error" style="padding-top:15px; display:none;">Please visit the new registration kiosk. You do not have an existing registration.</h3>').insertAfter('#login-title').show('slow');
					$('<a href="/checkin" class="button action-button href-action">Restart</button>').insertAfter('#here-submit').show('slow');
				} else if (html['status'] == 1) {
					$('<h3 class="fs-error" style="padding-top:15px; display:none;">Please see a YHack organizer to complete your registration.</h3>').insertAfter('#login-title').show('slow');
					$('<a href="/checkin" class="button action-button href-action">Restart</button>').insertAfter('#here-submit').show('slow');	
				} else {
					$('<input autocorrect="off" id="phone-field" class="validate[required,maxSize[75]]" name="phone" placeholder="Phone Name *" value="' + html['phone'] + '">').insertAfter('#login-title').show('slow');
					$('<input autocorrect="off" id="lastname-field" class="validate[required,maxSize[75]]" name="lastname" placeholder="Last Name *" value="' + html['lastname'] + '">').insertAfter('#login-title').show('slow');
					$('<input autocorrect="off" id="firstname-field" class="validate[required,maxSize[75]]" name="firstname" placeholder="First Name *" value="' + html['firstname'] + '">').insertAfter('#login-title').show('slow');
					$("#checkin").attr("action", "/checkin/checked");
					$('#checkin').ajaxFormUnbind();
					$('<input type="submit" id="here-submit" name="submit" class="submit action-button" value="Check In" />').insertAfter('#here-submit').show('slow');	
				}
			});
		}
	});
});