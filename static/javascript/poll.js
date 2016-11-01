function doPoll() {
	console.log('http://cs490-project.herokuapp.com/check_db?email=' + "{{ email }}");
	var post_html = 'http://cs490-project.herokuapp.com/check_db?email=' + $("#my-data").attr('data-name');
	console.log(post_html);
	$.post(post_html, function(data) {
	    console.log(data);
	    if (data === "1") {
	      location.href = 'http://cs490-project.herokuapp.com/success';
	    }
	    setTimeout(doPoll,500);
	});
}
$(document).ready(function() {
	console.log("here");
	doPoll();
})