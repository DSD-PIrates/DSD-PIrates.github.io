import MarkdownIt from 'markdown-it';
var md = new MarkdownIt();
var result = md.render('# markdown-it rulezz!');
console.log(result)
window.onload = function() {
    document.getElementById("mark").innerHTML = result
}