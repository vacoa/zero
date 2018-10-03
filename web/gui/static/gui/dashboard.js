$(document).ready( function () {
    var status;
    $.ajax({
        'url' : '../api/status',
        'type' : 'GET',
        'success' : function(data) {
            setstatus(data);
        }
      });
    
    loadbutton({'id':'#listenbutton',
                'url':'../api/listen',
                'txt':'ZE\nRO',
                'initfcn': function () {
                    $('#listenres').html('');
                    },
                'okfcn': function (data) {
                    $('#listenres').html(data.data.trans);
                    },
                'kofcn': function (data) {
                    $('#listenres').html('Sorry, I am busy. Please retry in a few seconds...');
                    }
                
        });

    loadbutton({'id':'#actionbutton',
                'url':'../api/action',
                'txt':'ZE\nRO',
                'initfcn': function () {
                    $('#actionres').html('');
                    },
                'okfcn': function (data) {
                    $('#actionres').html(JSON.stringify(data,null,2));
                    },
                'kofcn': function (data) {
                    $('#actionres').html(JSON.stringify(data,null,2));
                    }
                
        });
    
    function setstatus (service) {
        togglebutton({'id':'#togglebutton',
                'url':'../api/switchzero',
                'txton':'ON',
                'txtoff':'OFF',
                'initstate': service.sb,
                'initfcn': function () {
                    },
                'okfcn': function (data) {
                    },
                'kofcn': function (data) {
                    alert('Sorry, an error has occured. Please retry in a few seconds...');
                    }
                
        });
    }

});




