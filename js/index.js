var menulist = ["menu1", "menu2", "menu3", "menu4", "menu5"]

window.onload = function(){
    var text = ""
    for(var i = 0; i < menulist.length; i++) {
        text = text + '<td class="tableitem">' + menulist[i] + "</td>"
    }
    console.log(text)
    document.getElementById("toptable").innerHTML = text
    console.log(text)
}
