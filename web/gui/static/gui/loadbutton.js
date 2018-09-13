$(document).ready(() => {
	let $button = $('#listenbutton');
	$button.on('click', function() {
		var $this = $(this);
		if($this.hasClass('active') || $this.hasClass('success')) {
			return false;
		}
		$this.addClass('active');
		setTimeout(()=> {
			$this.addClass('loader');
		}, 125);
                $('#listenres').html('');
                $.ajax({
                    'url' : '../api/listen',
                    'type' : 'GET',
                    'success' : function(data) {
                        if (data.status=="ok") {
                            $('#listenres').html(data.data.trans);
                            $this.removeClass('loader active');
                            $this.text('OK');
                            $this.addClass('success animated pulse');
                        } else {
                            $('#listenres').html('Sorry, I am busy. Please retry in a few seconds...');
                            setTimeout(()=> {
                                $this.removeClass('loader active');
                                $this.text('KO');
                                $this.addClass('success animated pulse');
                            }, 150);
                            
                        }
                        setTimeout(()=> {
                                $this.text('ZE\nRO');
                                $this.removeClass('success animated pulse');
                                $this.blur();
                        }, 1300);
                    },
                  });               
	});
});