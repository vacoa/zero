function loadbutton(data) {
        let id = data.id;
        let url = data.url;
        let txt = data.txt;
        let initfcn = data.initfcn;
        let okfcn = data.okfcn;
        let kofcn = data.kofcn;
	let $button = $(id);
        $button.text = txt;
	$button.on('click', function() {
		var $this = $(this);
		if($this.hasClass('active') || $this.hasClass('success')) {
			return false;
		}
		$this.addClass('active');
		setTimeout(()=> {
			$this.addClass('loader');
		}, 125);
                initfcn();
                $.ajax({
                    'url' : url,
                    'type' : 'GET',
                    'success' : function(data) {
                        if (data.status=="ok") {
                            okfcn(data);
                            $this.removeClass('loader active');
                            $this.text('OK');
                            $this.addClass('success animated pulse');
                        } else {
                            kofcn(data);
                            setTimeout(()=> {
                                $this.removeClass('loader active');
                                $this.text('KO');
                                $this.addClass('success animated pulse');
                            }, 150);
                            
                        }
                        setTimeout(()=> {
                                $this.text(txt);
                                $this.removeClass('success animated pulse');
                                $this.blur();
                        }, 1300);
                    },
                });               
	});
}
