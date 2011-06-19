(function($) {
	$(document).ready(function() {
		speed = 'medium'
		$(".form-row.record").hide();
		$(".form-row.address").hide();
		$("#id_type").change(function() {
			if (this.value == "A" || this.value == "AAAA" || this.value == "PTR")
			{
				$(".form-row.record").slideUp(speed);
				$(".form-row.address").slideDown(speed);
			} else {
				$(".form-row.record").slideDown(speed);
				$(".form-row.address").slideUp(speed);
			}
		})
	})
})(django.jQuery)