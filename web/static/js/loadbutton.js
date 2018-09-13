$(document).ready(() => {
	let $button = $('.loadbutton');
	
	$button.on('click', function() {
		var $this = $(this);
                var txt = $this.html();
		if($this.hasClass('active') || $this.hasClass('success')) {
			return false;
		}
		$this.addClass('active');
		setTimeout(()=> {
			$this.addClass('loader');
		}, 125);
		setTimeout(()=> {
			$this.removeClass('loader active');
			$this.text('Ok');
			$this.addClass('success animated pulse');
		}, 1600);
		setTimeout(()=> {
			$this.text(txt);
			$this.removeClass('success animated pulse');
			$this.blur();
		}, 2900);
	});
});