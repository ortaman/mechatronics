
function scroll_to(clicked_link, nav_height) {
	var element_class = clicked_link.attr('href').replace('#', '.');
	var scroll_to = 0;
	if(element_class != '.top-content') {
		element_class += '-scroll';
		scroll_to = $(element_class).offset().top - nav_height;
	}
	if($(window).scrollTop() != scroll_to) {
		$('html, body').stop().animate({scrollTop: scroll_to}, 1000);
	}
}


$(document).ready(function() {
	/* Navigation */
	$('a.js-scroll-trigger').on('click', function(e) {
		e.preventDefault();
		console.log($('nav').outerHeight());
		scroll_to($(this), $('nav').outerHeight());
	});
});
