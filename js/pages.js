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
        //console.log(List)
        for(var i = 0; i < List.length; i++) {
            text = text + `<div class="day">` + 
            `<div class="postTitle"><a href="article.html?type=` + num + `&&pos=` + i + `">` + List[i].title + `</a></div>` +
            `<span class="postMeta">Posted on ` + List[i].time + `</span>`+ 
            `<div class="postCon"><div class="mainText">` + List[i].abstract + `</div><a href="article.html?type=` + num + `&&pos=` + i +  `">Read more.</a></div>`+ 
            `</div>`
        }
        //console.log(text)
        document.getElementById("articlelist").innerHTML = text
    })
}
/*
function loadTitle() {
    var text = ``
    readTextFile("js/information.json", (textDetail) => {
        TmpList = JSON.parse(textDetail)
        newsList = TmpList[0]
        docsList = TmpList[1]
        var num = 0
        for(var i = newsList.length - 1; i >= 0; i--) {
            text = text + `<p><span class="new">NEW!</span><a href="docs/` + newsList[i].src + `">` + newsList[i].title + `</a></p>`
            num++
            if(num >= 5) break;
        }
        document.getElementById("newstext").innerHTML = text
        text = ``
        num = 0
        for(var i = docsList.length - 1; i >= 0; i--) {
            text = text + `<p><span class="new">NEW!</span><a href="docs/` + docsList[i].src + `">` + docsList[i].title + `</a></p>`
            num++
            if(num >= 5) break;
        }
        document.getElementById("docstext").innerHTML = text
        
    })
}*/

function loadTitle() {
    var text = ``
    readTextFile("js/information.json", (textDetail) => {
        TmpList = JSON.parse(textDetail)
        newsList = TmpList[0]
        docsList = TmpList[1]
        var num = 0
        for(var i = newsList.length - 1; i >= 0; i--) {
            text = text + `<p><a href="docs/article.html?type=0&&pos=` + i + `">` + newsList[i].title + `</a></p>`
            num++
            if(num >= 3) break;
        }
        document.getElementById("newstext").innerHTML = text
        text = ``
        num = 0
        for(var i = docsList.length - 1; i >= 0; i--) {
            text = text + `<p><a href="docs/article.html?type=1&&pos=` + i + `">` + docsList[i].title + `</a></p>`
            num++
            if(num >= 3) break;
        }
        document.getElementById("docstext").innerHTML = text
        
    })
}