# GDSS v0.0.2
# Author: Bob

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# every data in HTTP request and response has this structure
SAMPLE_DATA = {
    "name": "test_gdss",
    "data": "here must be a string",
    "type": "here must be a string"
}
PING_DATA = {
    "name": "",
    "data": "",
    "type": "ping"
}

hostIp   = "0.0.0.0"
hostPort = 32767
host     = (hostIp, hostPort)

class Resquest(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get('content-length') is not None:
            try:
                datas = self.rfile.read(int(self.headers['content-length']))
                inputData = json.loads(datas.decode())
            except:
                inputData = PING_DATA
        else:
            inputData = PING_DATA

        data = getOutputDataByInput(inputData)
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        self.do_POST()
 
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
