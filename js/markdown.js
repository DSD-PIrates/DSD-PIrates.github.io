/*var md = window.markdownit({
    html: true,
    linkify: true,
    typographer: true,
  }).use(window.markdownitSub)
*/
function readTextFile(filePath, callback) {
    const xhrFile = new XMLHttpRequest();
    xhrFile.open("GET", filePath, true);
    xhrFile.onload  = function() {
        const allText = xhrFile.response;
        callback(allText)
    }
    xhrFile.send();
}

const filePath = `../md/BlogForWeek1.md`
var testpath = "../md/TestAll.md"

window.onload = function() {
    topbar()
    var converter = new showdown.Converter()
    readTextFile(testpath, (textDetail) => {
        console.log(textDetail)
        //var result = md.render(textDetail)
        var result = converter.makeHtml(textDetail)
        document.getElementById("markdown").innerHTML = result
    })
}