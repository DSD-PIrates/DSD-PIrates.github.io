var md = window.markdownit("default")

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

window.onload = function() {
    topbar()
    readTextFile(filePath, (textDetail) => {
        //console.log(textDetail)
        var result = md.render(textDetail)
        document.getElementById("markdown").innerHTML = result
        hljs.highlightAll()
    })
    
}