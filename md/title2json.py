import os
import json
import datetime

data = {}
file = "GDSS.md"

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