from http.server import HTTPServer, BaseHTTPRequestHandler
import json

host_ip = '0.0.0.0'
host = (host_ip, 8000)

class Resquest(BaseHTTPRequestHandler):
    def do_POST(self):

        if self.headers.get('content-length') is not None:
            datas = self.rfile.read(int(self.headers['content-length']))
            inputData = datas.decode()
        else:
            inputData = ""
        print(inputData)

        data = "fuck you!"

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        self.do_POST()
 
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
