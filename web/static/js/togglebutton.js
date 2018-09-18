function togglebutton(data) {
        let id = data.id;
        let url = data.url;
        let txton = data.txton;
        let txtoff = data.txtoff;
        let state = data.initstate;
        let initfcn = data.initfcn;
        let okfcn = data.okfcn;
        let kofcn = data.kofcn;
	let $button = $(id);
        if (state) {
            $button.addClass('active');
            $button.text(txton);
        } else {
            $button.addClass('inactive');
            $button.text(txtoff);
        }
	$button.on('click', function() {
		var $this = $(this);
		$this.addClass('loader');
                initfcn();
                $.ajax({
                    'url' : url,
                    'type' : 'GET',
                    'data': {'state' : !state},
                    'success' : function(data) {
                        if (data.status=="ok") {
                            okfcn(data.data);
                            if (state) {
                                $this.removeClass('loader active');
                                $this.addClass('inactive');
                                $this.text(txtoff);
                            } else {
                                $this.removeClass('loader inactive');
                                $this.addClass('active');
                                $this.text(txton);
                            }
                            state = !state;
                        } else {
                            kofcn(data.data);
                            setTimeout(()=> {
                                $this.removeClass('loader');
                            }, 150); 
                        }
                    },
                });               
	});
}