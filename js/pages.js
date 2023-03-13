function readTextFile(filePath, callback) {
    const xhrFile = new XMLHttpRequest();
    xhrFile.open("GET", filePath, true);
    xhrFile.onload  = function() {
        const allText = xhrFile.response;
        callback(allText)
    }
    xhrFile.send();
}

function loadList(num) {
    var text = ``
    readTextFile("../js/information.json", (textDetail) => {
        TmpList = JSON.parse(textDetail)
        List = TmpList[num]
        console.log(List)
        for(var i = 0; i < List.length; i++) {
            text = text + `<div class="day"><div class="postTitle"><a href="` + List[i].src + `">` + List[i].title + `</a></div><span class="postMeta">Posted on ` + List[i].time + `</span><div class="postCon"><div class="mainText">` + List[i].abstract + `</div><a herf="` + List[i].src + `">Read more.</a></div>`
        }
        console.log(text)
        document.getElementById("articlelist").innerHTML = text
    })
}
