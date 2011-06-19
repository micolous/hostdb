(function($) {
	$(document).ready(function() {
		speed = 'medium'
		$(".form-row.record").hide();
		$(".form-row.address").hide();
		$("#id_type").change(function() {
			if (this.value == "" || this.value == null)
			{
				$(".form-row.record").slideUp(speed);
				$(".form-row.address").slideUp(speed);
			}
			else if (this.value == "A" || this.value == "AAAA" || this.value == "PTR")
			{
				$(".form-row.record").slideUp(speed);
				$(".form-row.address").slideDown(speed);
			} else {
				$(".form-row.record").slideDown(speed);
				$(".form-row.address").slideUp(speed);
			}
		}).trigger('change')
	})
})(django.jQuery)
