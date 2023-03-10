var menulist = [
    ["首页"], 
    ["NEWS", "week5", "week4", "week3", "week2", "week1"],
    ["Members"],
    ["借用"],
    ["在线数据"]
]
var linklist = [
    ["#"],
    ["docs/test.html", "#", "#", "#", "#", "#"],
    ["docs/test.html"],
    ["#"],
    ["#"]
]

var caret = '<span class="caret"></span>'
var presentation_normal = '<li role="presentation">'
var presentation_dropdown = '<li role="presentation" class="dropdown">'
var dropdown_toggle_1 = '<a class="dropdown-toggle" data-toggle="dropdown" href="'
var dropdown_toggle_2 =  '" role="button" aria-haspopup="true" aria-expanded="false">'
var dropdown_menu = '<ul class="dropdown-menu">'
var toptext = `
<p style="font-size: x-large; text-align: center; margin: 0; padding-left: 10px; padding-right: 10px;">小组名-项目名</p>
<ul class="nav nav-pills" id="toptable">`

window.onload = function(){
    var text = ""
    for(var i = 0; i < menulist.length; i++) {
        var rlength = menulist[i].length
        if(rlength == 1) {
            text = text + presentation_normal + '<a href="' + linklist[i][0] + '">' + menulist[i][0] + '</a></li>'
        }
        else {
            text = text + presentation_dropdown + dropdown_toggle_1 + linklist[i][0] + dropdown_toggle_2 + menulist[i][0] + caret + '</a>' + dropdown_menu
            for(var j = 1; j < rlength; j++) {
                text = text + "<li>" + menulist[i][j] + "</li>"
            }
            text = text + "</ul></li>"
        }
        
    }
    text = text + '</ul>'
    console.log(text)
    document.getElementById("top").innerHTML = toptext + text
    //console.log(text)
}
