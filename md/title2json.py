import os
import json
import datetime

data = {}
file = r"md\WhiteBox Test Report.md"

with open(file, "r", encoding='utf-8') as f:
    content = f.read(250)
file_name = file.split("\\")[-1][:-3]
modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d %H:%M")
file_location = file.replace('\\', '/')
data = {
    "title": file_name,
    "src": file_location,
    "time": modified_time,
    "abstract": content.replace('\n', '')
}
with open("md/tmp.json", "w") as f:
    json.dump(data, f, indent=4)
