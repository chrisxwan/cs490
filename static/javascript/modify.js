$(document).ready(function() {

	$("img").error(function(){
  	$(this).css({ "opacity" : 0 });
	});

	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
    	$("head").append('<link href="/static/css/application-mobile.css" rel="stylesheet"><link href="/static/css/form-mobile.css" rel="stylesheet">');
	}

	$('#school-field').on('change', function() {
		if ($(this).val() == 'other'){
			$(this).parent().append('<input id="school-other-field" class="validate[required,maxSize[200]]" name="school-other-field" placeholder="School Name *">');
			$('#school-other-field').validationEngine('attach', {binded:false});
		} else if ($('#school-other-field').length) {
			$('#school-other-field').validationEngine('hideAll');
			$('#school-other-field').validationEngine('detach');
			$('#school-other-field').remove();
		}
	});

	// kludge for displaying client-side validation (purely UI)
	$("#resume-field").on('click', function(){
		$(this).addClass("validate[custom[falseFile]]");
	});
	$("#resume-field").on('change', function(){
		if (window.FileReader) {
		    var input = document.getElementById('resume-field');    
    		var file = input.files[0];
	  		if (file.size > 10 * 1024 * 1024){
	  			$("#resume-field").validationEngine('validate');
	  		} else {
	  			$("#resume-field").removeClass("validate[custom[falseFile]]");
	  		}
		} else {
			$("#resume-field").removeClass("validate[custom[falseFile]]");
		}
	});

	$("#submit").click(function(){
		// because select2 duplicates the class and I have no idea when it does so
		$(".select2-container").each(function(){
			$(this).removeClass("validate[required]");
		});
	});

	$(window).load(function(){
		var width = $("#modify").width() * .8 - parseInt($("fieldset").css("padding-left")) * 2 + "px";
		$("#school-field").select2({
			minimumInputLength: 2,
			width: width,
			matcher: function(term, text) {
				var terms = term.split(" ");
				for (var i =0; i < terms.length; i++){
					var tester = new RegExp("\\b" + terms[i], 'i');
					if (tester.test(text) == false){
						return (text === 'Other')
					}
				}
				return true;
		    },
		    sortResults: function(results) {
		        if (results.length > 1) {
		        	results.pop();
		        }
		        return results;
		    },
			containerCssClass: 'select2-container-inner-application',
			dropdownCssClass: 'select2-container-dropdown-application'
		});
		var val = $("#school-field").attr("value");
		$("#school-field").select2("val", val);
		if ($("#school-field").select2("val") != val){
			$("#school-field").select2("val", "other");
			$("#school-field").parent().append('<input id="school-other-field" class="validate[required,maxSize[200]]" name="school-other-field" placeholder="School Name *" value="' + val + '">');
			$('#school-other-field').validationEngine('attach', {binded:false});
		}

		$("#graduation-year-field").select2({
			width: width
		});
		var val = $("#graduation-year-field").attr("value");
		$("#graduation-year-field").select2("val", val);

		$(".select2-container").each(function(){
			var right = parseInt($("#modify input").css("padding")) * 2 + "px";
			$(this).siblings("input, select").attr('style', "left: auto !important; right: " + right + " !important;");
		});

		$('#modify').validationEngine('attach', {binded:false});
		
	});
});



