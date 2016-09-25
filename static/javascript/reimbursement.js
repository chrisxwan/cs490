$(document).ready(function(){

	$("img").error(function(){
    	$(this).css({ "opacity" : 0 });
  	});

	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
    	$("head").append('<link href="/static/css/application-mobile.css" rel="stylesheet"><link href="/static/css/form-mobile.css" rel="stylesheet">');
	}

	if ($('#reimbursement-method-field').val() != '') {
		$('#check-file').fadeIn();
	}

	$('#new-receipts-field').on('click', function() {
		$('#check-file').fadeOut(function() {
			$('#check-upload').fadeIn();
		});
	});

	var width = $("#submit-receipts").width() * .8 - parseInt($("fieldset").css("padding-left")) * 2 + "px";

	$('#reimbursement-method-field').select2({
		width: width,
		containerCssClass: 'select2-container-inner-application',
		dropdownCssClass: 'select2-container-dropdown-application'
	});

	$('#reimbursement-method-field').on('change', function() {
		if (!($('#check-file').is(":visible"))) {
			$('#check-upload').fadeIn();
		}
		
		if ($(this).val() == 'Venmo'){
			$('#check-information').fadeOut(function() {
				$('#venmo-information').fadeIn();
			});
		} else if ($(this).val() == 'Check'){
			$('#venmo-information').fadeOut(function() {
				$('#check-information').fadeIn();
			});
		}
	});

	$('#submit-receipts').on('submit', function(e) {
		var rType = $('#reimbursement-method-field').val();
        if (rType == 'Venmo'){
        	if ($("#venmo-id-field").validationEngine('validate') || $("#resume-field").validationEngine('validate')) {
        		return false;
     		}
        } else if (rType == 'Check') {
        	if ($("#address1-field").validationEngine('validate') || $("#address2-field").validationEngine('validate') || 
        		$("#city-field").validationEngine('validate') || $("#state-field").validationEngine('validate') || 
        		$("#zip-field").validationEngine('validate') || $("#resume-field").validationEngine('validate')) {
        		return false;
        	}
        } else {
        	if ($('#reimbursement-method-field').validationEngine('validate')) {
        		return false;
        	}
        }
    });
});

