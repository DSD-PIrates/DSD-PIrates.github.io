import os
import json
import datetime

data = {}
file = "centerResearch on end-to-end latency between different devices.md"

with open(file, "r") as f:
    content = f.read(250)
file_name = file[:-3]
modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d %H:%M")
file_location = file[:-3] + '.html'
data = {
    "title": file_name,
    "src": file_location,
    "time": modified_time,
    "abstract": content
}
with open("tmp.json", "w") as f:
    json.dump(data, f, indent=4)
txt = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="shortcut icon" href="../img/raspberrypi.ico">
    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="../css/index.css" >
    <link rel="stylesheet" type="text/css" href="../css/blog.css" >
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
    
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top top" id="top"></nav>
    <div class="container bs-docs-container">
        <div class="row">
            <div class="col-md-10 blog" role="main">
                <div id="markdown"></div>
            </div>
            <div class="col-md-2 toc" role="main">
                <div id="toc"></div>
            </div>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha256-ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ=" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/markdown-it@13.0.1/dist/markdown-it.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            showProcessingMessages: false,
            messageStyle: "none",
            extensions: ["tex2jax.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
                inlineMath:  [ ["$", "$"] ],
                displayMath: [ ["$$","$$"] ],
                skipTags: ['script', 'noscript', 'style', 'textarea', 'pre','code','a'],
                ignoreClass:"comment-content"
            },
            "HTML-CSS": {
                availableFonts: ["STIX","TeX"],
                showMathMenu: false
            }
        });
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
        </script>
        <script src="//cdn.bootcss.com/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
    <script src="../js/index.js"></script>
    <script src="../js/markdown.js"></script>
    <script>topbar({id})</script>
    <script>LoadMarkdown("../md/{filename}")</script>
</body>
</html>
'''.format(title=data.title, id = 0, filename=file)
with open("../docs/" + data.src, "w") as f:
    f.write(txt)