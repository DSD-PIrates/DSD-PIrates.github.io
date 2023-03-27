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

var abLevel = 0

// 函数的含义是，在第index个标题处生成目录树，该标题级别为hLevel
function genFromTitle(hLevel, index){
	let ele = ''
	while (index < $('.isTitle').length) {
		let t = $('.isTitle').eq(index)
		if (t.attr('hLevel') > hLevel) {
			// 遇到更小的标题，递归生成
			let nt = genFromTitle(t.attr('hLevel'), index)
			//ele += `<li>${nt.ele}</li>`
			ele += nt.ele
			// 从nt.index到index-1的标题都处理完毕，更新index
			index = nt.index 
		}
		else if (t.attr('hLevel') < hLevel) break // 遇到更大的标题，向上返回
		else {
			t.attr('id', 'tp'+index) // 恰好每个标题有唯一index 直接拿来用
			tmp = ''
			for(var i = 0; i < hLevel - 1 - abLevel; i++) {
				tmp = tmp + '&nbsp;&nbsp;'
			}
	        ele = ele +  '<li>' + tmp + `<a href="#tp${index}"> ${ t.text() } </a></li>`;
	        index ++;
		}
	}
	//ele = `<ul>${ele}</ul>`
	return {ele, index} //index 也要返回去，父函数继续往后生成
}

// 定义一个函数，用于判断一个元素是否在窗口范围内
function isInViewport(element) {
    var rect = element.getBoundingClientRect();
    return (
        rect.top >= -10 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) +10
    );
}

// 定义一个函数，用于高亮当前章节对应的目录项
function highlightToc() {
    // 获取所有的目录链接元素
    var links = document.querySelectorAll("#toc li a");
	var linkbars = document.querySelectorAll("#toc li");
    // 遍历所有的目录链接元素，取消高亮样式，并找到第一个在视口范围内的锚点对应的链接元素，添加高亮样式
	var lighting = -1
	
    for (var i=0; i<links.length; i++) {
		//console.log(lighting)
		if(links[i].classList.contains("active") && lighting == -1) {
			lighting = i;
		} else if(links[i].classList.contains("active") && lighting > -1) {
			links[lighting].classList.remove("active");
	  		linkbars[lighting].classList.remove("active");
			links[i].classList.remove("active");
	  		linkbars[i].classList.remove("active");
		} else{
			links[i].classList.remove("active");
	  		linkbars[i].classList.remove("active");
		}
      	
    }
	for (var i=0; i<links.length; i++) {
		var anchorId=links[i].getAttribute("href").slice(1);
		var anchor=document.getElementById(anchorId);
		if(isInViewport(anchor)){
		  links[i].classList.add("active");
		  linkbars[i].classList.add("active");
		  console.log($(linkbars[i]).offset())
		  if($(linkbars[i]).offset().top > 4500) {
			console.log('upupup')
			$(linkbars[i]).scrollTop(1000);
		  } else {
			$(linkbars[i]).scrollTop(0);
		  }
		  break;
		}
	  }
}

// 在页面加载完成后，调用highlightToc函数
window.addEventListener("load", highlightToc);

// 在页面滚动时，调用highlightToc函数
window.addEventListener("scroll", highlightToc);
 
// elEssay为文档挂载点，elContent为生成的目录挂载点
function makeEssayContent(elEssay, elContent) {
	// 首先标记所有标题
	var flag = 0
	for (let i = 1; i <= 6; i++) {
		elEssay.find('h'+i).addClass('isTitle').attr('hLevel', i)
		if(elEssay.find('h'+i).length < 1 && flag == 0) {
			abLevel++
		} else {
			flag = 1
		}
        //console.log(elEssay.find('h'+i))
	}
    //console.log(genFromTitle(1, 0).ele)
	elContent.html("<ul>" + genFromTitle(1, 0).ele + "</ul>");//从第一个一级标题开始生成
}
/*
function setWidthofToc() {
	console.log(getComputedStyle(document.querySelector('.blog')).width)
	var widthInPercentage = parseFloat(getComputedStyle(document.querySelector('.col-md-10')).width)
	console.log(widthInPercentage)
	document.querySelector('.toc').style.maxWidth = (100 - widthInPercentage) + "%"
}
*/
function LoadMarkdown(filepath) {
    readTextFile(filepath, (textDetail) => {
		var prefilepaths = filepath.split("/")
		var prefilepath = ""
		for(var i = 0; i < prefilepaths.length - 1; i++) {
			prefilepath = prefilepath + prefilepaths[i] + '/'
		}
        //console.log(prefilepath)
        var result = md.render(textDetail)
		result = result.replace(/\.\//g, prefilepath)
		result = result.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"')
		//console.log(result)
        document.getElementById("markdown").innerHTML = result
        hljs.highlightAll()
        makeEssayContent($("#markdown"), $("#toc"))
		//setWidthofToc()
    })
}

