from http.server import HTTPServer, BaseHTTPRequestHandler
import json

import GDSC

host_ip = '0.0.0.0'
host = (host_ip, 1638)

KNOWN_FILE_LIST = ["index.html"]

def getFile(filename):
    assert type(filename) == str
    try:
        fp = open(filename)
        context = fp.read()
    except:
        context = "<h1>File Not Found</h1>"
    return context

def matchPrefix(path, pre):
    assert type(path) == str
    assert type(pre) == str
    assert len(pre) > 0

    if len(path) < len(pre):
        return False
    else:
        return path[:len(pre)] == pre

def getJsonData(path):
    assert type(path) == str
    assert matchPrefix(path, "/jsonData/")
    
    deviceName = path[len("/jsonData/") : ]
    if deviceName == "":
        return json.dumps({
            "result": "deviceName can not be empty"
        })
    else:
        if deviceName.find("/") != -1:
            deviceName, maxn = deviceName.split("/", 1)
            try:
                maxn = int(maxn)
            except:
                maxn = 1
        else:
            maxn = 1
        return GDSC.readDataFromServer(deviceName, maxn)

def getStringByPath(path):
    if path is None or type(path) != str:
        return "<h1>path is not a string</h1>"
    else:
        print(path)

        if path[1:] in KNOWN_FILE_LIST:
            return getFile(path[1:])
        elif matchPrefix(path, "/jsonData/"):
            return getJsonData(path)

        return "<h1>path is unknown</h1>"

class Resquest(BaseHTTPRequestHandler):    
    def do_GET(self):
        obj_tosend = getStringByPath(self.path)
        obj_tosend = obj_tosend.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', len(obj_tosend))
        self.end_headers()
        self.wfile.write(obj_tosend)
 
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
