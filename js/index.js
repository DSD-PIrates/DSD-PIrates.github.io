var menulist = [
    [{ name: "Home", src: "index.html" }],
    [
        /*{name: "News", src: ""}, 
        {name: "Website Construction Record", src: "docs/Website Construction Record.html"},
        {name: "Research on end-to-end latency between different devices", src: "docs/Research on end-to-end latency between different devices.html"}, 
        {name: "BlogForWeek1", src: "docs/BlogForWeek1.html"}, 
        {name: "More", src: "docs/news.html"}*/
    ], [
        /*{name: "Documents", src: ""}, 
        {name: "Software Requirements Specification (SRS)", src: "docs/Software Requirements Specification (SRS).html"},
        {name: "End-to-end latency between different devices", src: "docs/End-to-end latency between different devices.html"}, 
        {name: "GDSS", src: "docs/GDSS.html"}, {name: "More", src :"docs/documents.html"}*/
    ],
    [{ name: "Members", src: "docs/member.html" }],
    [{ name: "Borrowing", src: "docs/borrow.html" }],
    [{ name: "Online", src: "docs/realtimedata.html" }]
]
//{name: "", src: "docs/.html"},
var caret = '<span class="caret"></span>'
var presentation_normal = '<li class="nav-item">'
var presentation_dropdown = '<li class="nav-item dropdown">'
var dropdown_toggle_1 = '<a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="'
var dropdown_toggle_2 = '" role="button" aria-expanded="false">'
var dropdown_menu = '<ul class="dropdown-menu" aria-labelledby="navbarDropdown">'
var toptext = `
<div class="navbar-brand">PIrates-Raspberry Pi</div>
<button type="button" class="navbar-toggler" data-bs-toggle="collapse"
    data-bs-target="#collapsed-nav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="collapsed-nav">
    <ul class="navbar-nav">`
function readTextFile(filePath, callback) {
    const xhrFile = new XMLHttpRequest();
    xhrFile.open("GET", filePath, true);
    xhrFile.onload = function () {
        const allText = xhrFile.response;
        callback(allText)
    }
    xhrFile.send();
}


async function readMenuList(textDetail) {
    var TmpList = JSON.parse(textDetail)
    for (var j = 0; j < 2; j++) {
        var _list = []
        var _num = 0
        if (j == 0) {
            _list.push({ name: "News", src: "" })
        } else {
            _list.push({ name: "Docs", src: "" })
        }
        for (var i = TmpList[j].length - 1; i >= 0 && _num < 5; i--) {
            var title = TmpList[j][i].title
            _list.push({ name: title, src: "docs/article.html?type=" + j + "&&pos=" + i })
            _num++
        }
        if (j == 0) {
            _list.push({ name: "More", src: "docs/news.html" })
        } else {
            _list.push({ name: "More", src: "docs/documents.html" })
        }
        menulist[1 + j] = _list
    }
}

function isNormalPage(flag) {
    if (flag == 0) {
        return ""
    } else {
        return "../"
    }
}

async function topbar(flag) {
    readTextFile("../js/information_nd.json", function (arg) {
        readMenuList(arg);
        var text = ""
        for (var i = 0; i < menulist.length; i++) {
            var rlength = menulist[i].length
            if (rlength == 1) {
                text = text + presentation_normal + '<a class="nav-link" href="' + isNormalPage(flag) + menulist[i][0].src + '">' + menulist[i][0].name + '</a></li>'
            }
            else {
                text = text + presentation_dropdown + dropdown_toggle_1 + isNormalPage(flag) + menulist[i][0].src + dropdown_toggle_2 + menulist[i][0].name + caret + '</a>' + dropdown_menu
                for (var j = 1; j < rlength; j++) {
                    text = text + '<li><a class="dropdown-item" href="' + isNormalPage(flag) + menulist[i][j].src + '">' + menulist[i][j].name + "</a></li>"
                }
                text = text + "</ul></li>"
            }

        }
        text = text + `</ul></ul></div>`
        console.log(text)
        document.getElementById("top").innerHTML = toptext + text
    })
}