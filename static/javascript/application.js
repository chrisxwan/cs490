$(document).ready(function() {
	$("img").error(function(){
    	$(this).css({ "opacity" : 0 });
  	});

	if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
    	$("head").append('<link href="static/css/application-mobile.css" rel="stylesheet"><link href="static/css/form-mobile.css" rel="stylesheet">');
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


	var last_tab = false;
	$(window).keydown(function(event){
	    if(event.keyCode == 13 && !last_tab) {
	      event.preventDefault();
	      if ($('.active').length == 1){
	      	$(".next")[0].click();
	      } else if ($('.active').length == 2) {
	      	$(".next")[1].click();
	      }
	      return false;
	    } else {
	    	return true;
	    }
	});

	var current_fs, next_fs, previous_fs; //fieldsets
	var left, opacity, scale; //fieldset properties which we will animate
	var animating; //flag to prevent quick multi-click glitches

	$(".next").click(function(){

		// because select2 duplicates the class and I have no idea when it does so
		$(".select2-container").each(function(){
			$(this).removeClass("validate[required]");
		});

		if(animating) return false;
		animating = true;
		
		current_fs = $(this).parent();
		next_fs = $(this).parent().next();
		if ($("fieldset").index(current_fs) == 0) {
			if ($("#email-field").validationEngine('validate') || $("#password-field").validationEngine('validate') || $("#password-check-field").validationEngine('validate')) {
				animating = false;
				return false;
			}
		} else if ($("fieldset").index(current_fs) == 1) {
			if ($("#firstname-field").validationEngine('validate') || $("#lastname-field").validationEngine('validate') || $("#graduation-year-field").validationEngine('validate') || $("#gender-field").validationEngine('validate') || $("#major-field").validationEngine('validate') || $("#school-field").validationEngine('validate')) {
				animating = false;
				return false;
			}
			if ($("#school-other-field").length > 0 && $("#school-other-field").validationEngine('validate')){
				animating = false;
				return false;
			}
		}


		if ($("fieldset").index(next_fs) == 2){
			last_tab = true;
		}
		//activate next step on progressbar using the index of next_fs
		$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
		
		//show the next fieldset
		// next_fs.show(); 
		next_fs.css({ "opacity" : "1", "z-index" : "1" });
		//hide the current fieldset with style
		current_fs.animate({opacity: 0}, {
			step: function(now, mx) {
				//as the opacity of current_fs reduces to 0 - stored in "now"
				//1. scale current_fs down to 80%
				scale = 1 - (1 - now) * 0.2;
				//2. bring next_fs from the right(50%)
				left = (now * 50)+"%";
				//3. increase opacity of next_fs to 1 as it moves in
				opacity = 1 - now;
				current_fs.css({'transform': 'scale('+scale+')'});
				next_fs.css({'left': left, 'opacity': opacity});
			}, 
			duration: 800, 
			complete: function(){
				// current_fs.hide();
				current_fs.css({ "opacity" : "0" , "z-index" : "-1" });
				animating = false;
			}, 
			//this comes from the custom easing plugin
			easing: 'easeInOutBack'
		});
	});

	$(".previous").click(function(){

		$(".select2-container").each(function(){
			$(this).removeClass("validate[required]");
		});


		if(animating) return false;
		animating = true;
		
		current_fs = $(this).parent();
		previous_fs = $(this).parent().prev();

		last_tab = false;
		
		//de-activate current step on progressbar
		$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
		
		//show the previous fieldset
		// previous_fs.show();
		previous_fs.css({ "opacity" : 1 , "z-index" : 1 });
		//hide the current fieldset with style
		current_fs.animate({opacity: 0}, {
			step: function(now, mx) {
				//as the opacity of current_fs reduces to 0 - stored in "now"
				//1. scale previous_fs from 80% to 100%
				scale = 0.8 + (1 - now) * 0.2;
				//2. take current_fs to the right(50%) - from 0%
				left = ((1-now) * 50)+"%";
				//3. increase opacity of previous_fs to 1 as it moves in
				opacity = 1 - now;
				current_fs.css({'left': left});
				previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
			}, 
			duration: 800, 
			complete: function(){
				// current_fs.hide();
				current_fs.css({ "opacity" : "0" , "z-index" : -1 });
				animating = false;
			}, 
			//this comes from the custom easing plugin
			easing: 'easeInOutBack'
		});
	});

	$(window).load(function(){
		var width = $("#apply").width() * .8 - parseInt($("fieldset").css("padding-left")) * 2 + "px";
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
	        	// var tester = new RegExp("\\b" + term, 'i');
	        	// return (text === 'Other') || (tester.test(text));
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

		$("#graduation-year-field").select2({
			width: width
		});

		$("#gender-field").select2({
			width: width
		});

		$("#previous-hackathons-field").select2({
			width: width
		});

		$("#race-field").select2({
			width: width
		});

		$(".select2-container").each(function(){
			var right = parseInt($("#apply input").css("padding")) * 2 + "px";
			$(this).siblings("input, select").attr('style', "left: auto !important; right: " + right + " !important;");
		});

		$('#apply').validationEngine('attach', {binded:false});
		
	});
});



