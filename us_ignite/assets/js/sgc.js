(function ($) {
	$(function () {
		$(document).foundation();

		$( "#menu-button" ).click(function() {     
			var $elems = $('.jump-to-container, .social-bar');
			if ( $elems.hasClass("active"))
			{
				$elems.removeClass("active");
			}
			else
			{
				$elems.addClass("active");
			}
		});

		$("div.video").fitVids();

		$("#jump-to-pitch").on("change", function (e) {
			var val = $(this).val();
			$("html, body").animate({ scrollTop: $('#' + val).offset().top }, 700);

		});

		$("#back-to-top span").on("click", function (e) {
			
			$("html, body").animate({ scrollTop: "0"}, 700);

		});

		var controller = new ScrollMagic.Controller();

		// build scene
		var scene = new ScrollMagic.Scene({
				triggerElement: "#footer-cta",
				reverse:false,
				offset: -300
			})
			.setTween("#footer-cta-content", 0.5, {opacity: 1, scale: 1}) // trigger a TweenMax.to tween
			.addTo(controller);
	});

})(jQuery);