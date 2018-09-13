$(document).ready( function () {
var last = []
$.ajax({
    'url' : '../api/summary',
    'type' : 'GET',
    'success' : function(data) {
        buildTable(data)
    },
    "complete" : function(result, status){
        resizeTable(avail);
    }
  });
$( function() {
   $( "#resizable" ).resizable();
} );
});


$( window ).resize(function () {
    resizeTable(avail);
});

function resizeTable(avail) {
    var stab = avail*3/4;
    $("#sumcell .dataTables_wrapper").width(stab);
    var prevavail = avail-stab-parseInt($("#prevcell").css("padding-right"))-parseInt($(".wrapper").css("padding-right"));
    $("#preview").width(prevavail) ;
    $("#prevcell .dataTables_wrapper").width(prevavail) ;
}

function buildTable(data) {
    var col = [];
    var headerHtml = '<tr><th>';
    var footerHtml = '<tr><th>';
    for (var i=0; i<data.columns.length; i++) {
        col.push(data.columns[i].data);
        headerHtml = headerHtml + data.columns[i].data;
        footerHtml = footerHtml + '<input type="text" placeholder="'+data.columns[i].data+'" data-index="'+i+'" style="width:95%;"/>'
        if (i < data.columns.length-1) {
            headerHtml = headerHtml + '</th><th>';
            footerHtml = footerHtml + '</th><th>';
        }
    }
    headerHtml = headerHtml + '</th></tr>';
    footerHtml = footerHtml + '</th></tr>';
    var groupColumn = 0;

    // Setup header and footer
    $("#tabHeader").html(headerHtml);
    $('#tabFooter').html(footerHtml);

    // Table
    var table = $('#tab').DataTable({
        "data": data.content,
        "columns": data.columns,
        "select": {
            style: 'multi+shift'
        },
        "order": [[ groupColumn, 'asc' ]],
        "scrollX": true,
        "scrollY": 600,
        "scrollCollapse": true,
        "paging": false,
        "columnDefs": [
            { "visible": false, "targets": groupColumn }
        ],
        "dom": '<"tabButton"B>lfrtip',
        "buttons": [
            {
            extend: 'collection',
            text: 'Download',
            buttons: [
                {
                extend: 'selected',
                text: 'Shape Dataset',
                action: function ( e, dt, button, config ) {
                    var rdata = dt.rows( { selected: true } ).data();
                    var listdata = [];
                    var maxshape = 20;
                    if (rdata.length<=maxshape) {
                        for (var i = 0; i < rdata.length; i++) {
                            listdata.push(rdata[i].folder + '\\' + rdata[i].shapeFile);
                        }
                        $.ajax({
                            'url' : '../api/dataset',
                            'data': {"listdata": listdata},
                            'type' : 'GET',
                            'xhr': function () {
                                var xhr = $.ajaxSettings.xhr();
                                xhr.onprogress = function (e) {
                                    if (e.lengthComputable) {
                                        var val = e.loaded / e.total * 100;
                                        $( "#progressbar" ).progressbar({value: val});
                                        $( ".progress-label" ).text(e.loaded/1000000 + ' / ' + e.total/1000000 + ' MB');
                                    }
                                };
                                return xhr;
                            },
                            'xhrFields': {
                                  responseType : 'blob'
                            },
                            'beforeSend': function () {
                                $( "#progressbar" ).progressbar({value: 0 });
                                $( ".progress-label" ).text("Sending request...");
                                $("#progressbar").show();
                            },
                            'success' : function(data) {
                                var filename = 'dataset.zip';
                                if (typeof window.chrome !== 'undefined') {
                                    // Chrome version
                                    var link = document.createElement('a');
                                    link.href = window.URL.createObjectURL(data);
                                    link.download = filename;
                                    link.click();
                                } else if (typeof window.navigator.msSaveBlob !== 'undefined') {
                                    // IE version
                                    var blob = new Blob([data], { type: 'application/zip' });
                                    window.navigator.msSaveBlob(blob, filename);
                                } else {
                                    // Firefox version
                                    var file = new File([data], filename, { type: 'application/zip' });
                                    window.open(URL.createObjectURL(file));
                                }
                            },
                            'error' : function(xhr, ajaxOptions, thrownError) {
                                alert('Oops... ' + thrownError + ' (' + xhr.status + ')');
                            },
                            'complete' : function(data) {
                                $( "#progressbar" ).hide();
                            }
                          });
                    } else {
                        alert('Cannot download more than ' + maxshape + ' shapes.');
                    }
                }
                },
                {
                extend: 'csv',
                text: 'Table as CSV'
                }
            ],
            fade: true,
            autoClose: true
            },
            {
            extend: 'collection',
            text: 'Columns',
            buttons: [
                {
                extend: 'colvis',
                columns: ':gt(1)',
                text: 'Choose'
                },
                {
                text: 'Tag',
                action: function ( e, dt, node, config ) {
                    showColumns(dt,['.root','.tag']);
                    }
                },
                {
                text: 'Default',
                action: function ( e, dt, node, config ) {
                    showColumns(dt,['.root','.default']);
                    }
                },
                {
                extend: 'colvisGroup',
                text: 'Show all',
                show: ':gt(1)'
                }
            ],
            fade: true,
            autoClose: true
            },
            {
            extend: "selectAll",
            text: "Select All"
            },
            {
            extend: "selectNone",
            text: "Deselect All"
            },
            {
            extend: 'selected',
            text: 'Refresh Details',
            action: function ( e, dt, button, config ) {
                var rdata = dt.rows(last).data();
                $.ajax({
                    'url' : '../api/preview',
                    'data': {
                        "folder": rdata[0].folder,
                        "shapeFile": rdata[0].shapeFile,
                    },
                    'line': rdata[0],
                    'type' : 'GET',
                    'success' : function(data) {
                        buildPreview(this.line,data);
                        avail = resize();
                        resizeTable(avail);
                    }
                  });
                }
            }


        ],
        "drawCallback": function ( settings ) {
            var api = this.api();
            var rows = api.rows( {page:'current'} ).nodes();
            var last=null;

            api.column(groupColumn, {page:'current'} ).data().each( function ( group, i ) {
                if ( last !== group ) {
                    $(rows).eq( i ).before(
                        '<tr class="group" style="background-color: #336699; color: white"><td colspan="' +  col.length.toString() + '">'+group+'</td></tr>'
                    );

                    last = group;
                }
            } );
        }
    } );

    // Filter event handler
    $( table.table().container() ).on( 'keyup', 'tfoot input', function () {
        table
            .column( $(this).data('index') )
            .search( this.value )
            .draw();
    } );

    // Remember last selected
    table.on( 'select', function ( e, dt, type, indexes ) {
    if ( type === 'row' ) {
        last = indexes;
        // do something with the ID of the selected items
    }
    } );

    // Order by the grouping
    $('#tbody').on( 'click', 'tr.group', function () {
        var currentOrder = table.order()[0];
        if ( currentOrder[0] === groupColumn && currentOrder[1] === 'asc' ) {
            table.order( [ groupColumn, 'desc' ] ).draw();
        }
        else {
            table.order( [ groupColumn, 'asc' ] ).draw();
        }
    } );

}

function showColumns(table,classes) {
    table.columns().visible( false, false );
    for ( var i=0 ; i<classes.length ; i++ ) {
        table.columns(classes[i]).visible( true, false );
    }
    table.columns.adjust().draw( false ); // adjust column sizing and redraw
}

function buildPreview(line,data) {
    if (data.status=="true") {
        $('#preview').html('<img src="data:image/png;base64,' + data.base + '" alt="shape" width="100%" height="150px"/>');
    } else {
        $('#preview').html('&#9658; No preview available...');
    }
    cont = [];
    for (var key in line) {
        cont.push({"name":key,"value":line[key]})
    }
    var table = $('#prevtab').DataTable({
        "data": cont,
        "columns": [{"data":"name"},
                     {"data":"value"}],
        "pageLength": 7,
        "destroy": true,
        "dom": 'frtp',
        "scrollX": true
    } );
    var frame = [];
    var first = null;
    var last = null;
    var tmp = [];
    if (("firstStartPos" in line) && (line.firstStartPos != "") && (line.firstStartPos != "[lat,long]")) {
        first = line.firstStartPos;
        first = first.split('[')[1].split(']')[0].split(',');
    }
    if (("lastStartPos" in line) && (line.lastStartPos != "") && (line.lastStartPos != "[lat,long]")) {
        last = line.lastStartPos;
        last = last.split('[')[1].split(']')[0].split(',');
    }
    if ((first != null) && (last != null)) {
        frame = '<iframe width="100%" height="300px" id="gmap_canvas" src="https://maps.google.com/maps?saddr=' + first[0] + ',' + first[1] + '&daddr=' + last[0] + ',' + last[1] + '&t=m&z=13&ie=UTF8&iwloc=addr&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>';
    } else if (first != null) {
        frame = '<iframe width="100%" height="300px" id="gmap_canvas" src="https://maps.google.com/maps?q=' + first[0] + ',' + first[1] + '&t=m&z=13&ie=UTF8&iwloc=addr&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>';
    } else if (last != null) {
        frame = '<iframe width="100%" height="300px" id="gmap_canvas" src="https://maps.google.com/maps?q=' + last[0] + ',' + last[1] + '&t=m&z=13&ie=UTF8&iwloc=addr&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>';
    } else {
        frame = '&#9658; No location available...';
    }
    $("#position").html(frame);
}

