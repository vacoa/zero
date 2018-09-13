$(document).ready( function () {
    var avail = resize();
});

$( window ).resize(function () {
    avail = resize();
});

function resize() {
    // Values to align with CSS
    var smallwin=600;
    var midwin=900;
    var bigwin=1900;
    // Variables got automatically from CSS

    var win = $( window ).width();
    if (win <= smallwin) {
        var contWidth = win;
    } else if (win <= midwin) {
        var contWidth = win-20;
    } else if (win > bigwin) {
        var contWidth = 1800;
    } else {
        var contWidth = win-40;
    }

    var sumWrapperPadding = parseInt($(".wrapper").css("padding-left")) + parseInt($(".wrapper").css("padding-right"));

    // Resize
    $(".header").width(contWidth) ;
    $(".topnav").width(contWidth) ;
    $(".main").width(contWidth) ;
    $(".footer").width(contWidth) ;
    avail = contWidth-sumWrapperPadding;
    return avail;

}

function menu(id) {
    comp = [
        {id:"navhome",href:"./home",title:"Home"},
        {id:"navboard",href:"./dashboard",title:"Dashboard"},
        {id:"navman",href:"./manual",title:"Manual"},
        {id:"navabout",href:"./about",title:"About"}
    ];
    var str = '';
    var cla = '';
    for (var i = 0; i<comp.length; i++) {
        if (id==comp[i].id) {
            cla = 'active';
        } else {
            cla = '';
        }
        str = str + '<a id="'+ comp[i].id +'" class="'+ cla +'" href="'+ comp[i].href +'">'+ comp[i].title +'</a>';
    }
    str = str + '<a href="javascript:void(0);" class="icon" onclick="menutoggle()"><i class="fa fa-bars"></i></a>'
    $(".topnav").html(str);
}

function menutoggle() {
    var x = document.getElementById("mytopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}
