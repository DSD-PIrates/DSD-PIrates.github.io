var menulist = [
    [{name: "Home", src: "index.html"}],
    [
        {name: "NEWS", src: ""}, 
        {name: "BlogForWeek1", src: "docs/BlogForWeek1.html"}, 
        {name: "More", src: "docs/news.html"}
    ],[
        {name: "Documents", src: ""}, 
        {name: "Research on end-to-end latency between different devices", src: "docs/Research on end-to-end latency between different devices.html"}, 
        {name: "GDSS", src: "docs/GDSS.html"}, {name: "More", src :"docs/documents.html"}
    ],
    [{name: "Members", src: "docs/member.html"}],
    [{name: "Things", src: "docs/borrow.html"}],
    [{name: "Online", src: "docs/realtimedata.html"}]
]

var caret = '<span class="caret"></span>'
var presentation_normal = '<li class="nav-item">'
var presentation_dropdown = '<li class="nav-item dropdown">'
var dropdown_toggle_1 = '<a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="'
var dropdown_toggle_2 =  '" role="button" aria-expanded="false">'
var dropdown_menu = '<ul class="dropdown-menu" aria-labelledby="navbarDropdown">'
var toptext = `
<div class="navbar-brand">PIrates-RoseberryPi</div>
<button type="button" class="navbar-toggler" data-bs-toggle="collapse"
    data-bs-target="#collapsed-nav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="collapsed-nav">
    <ul class="navbar-nav">`

function isNormalPage(flag) {
    if(flag == 0) {
        return ""
    } else {
        return "../"
    }
}

function topbar(flag) {
    var text = ""
    for(var i = 0; i < menulist.length; i++) {
        var rlength = menulist[i].length
        if(rlength == 1) {
            text = text + presentation_normal + '<a class="nav-link" href="' + isNormalPage(flag) + menulist[i][0].src + '">' + menulist[i][0].name + '</a></li>'
        }
        else {
            text = text + presentation_dropdown + dropdown_toggle_1 + isNormalPage(flag) + menulist[i][0].src + dropdown_toggle_2 + menulist[i][0].name + caret + '</a>' + dropdown_menu
            for(var j = 1; j < rlength; j++) {
                text = text + '<li><a class="dropdown-item" href="' + isNormalPage(flag) + menulist[i][j].src + '">' + menulist[i][j].name + "</a></li>"
            }
            text = text + "</ul></li>"
        }
        
    }
    text = text + `</ul></ul></div>`
    console.log(text)
    document.getElementById("top").innerHTML = toptext + text
}