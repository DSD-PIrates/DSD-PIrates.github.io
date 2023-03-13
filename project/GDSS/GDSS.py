from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import hashlib

import Dumper

host_ip = '0.0.0.0'
host = (host_ip, 8192)
MAX_VALUE_CNT = 100
SERVER_PASSWORD = "GDSS-GGN-2015"

DB_JSON_NAME = "db.json"
TYPE_LIST = ["ping", "read", "write"]

def deepCopy(req): # to deep copy an object
    if type(req) == dict:
        ans = {}
        for x in req:
            ans[x] = req[x]
        return ans
    elif type(req) == list:
        ans = []
        for x in req:
            ans.append(x)
        return ans
    else:
        return req
    
def loadDB(filename):
    assert type(filename) == str
    suc_flag = True
    mem = {}
    try:
        with open(filename) as f:
            mem = json.load(f)
    except:
        suc_flag = False
    return mem, suc_flag

def saveDB(mem, filename):
    assert type(filename) == str
    suc_flag = True
    try:
        with open(filename, "w") as f:
            json.dump(mem, f, indent=4)
    except:
        suc_flag = False
    return suc_flag

def getMd5(s: str):
    assert type(s) == str
    str_to_encode = s
    md5_obj = hashlib.md5()
    md5_obj.update(str_to_encode.encode('utf-8'))
    md5_code = md5_obj.hexdigest()
    return str(md5_code)

def checkHashCorrect(req):
    assert type(req) == dict
    assert req.get("hash") is not None and type(req.get("hash")) == str

    # check hash value here
    req_copy = deepCopy(req)
    req_copy["hash"] = SERVER_PASSWORD
    hash_value = getMd5(Dumper.MyDumps(req_copy))
    if hash_value == req["hash"]:
        return True
    else:
        return False

def getReadData(req):
    assert type(req) == dict
    assert req.get("type") == "read"
    if req.get("name") is None or type(req.get("name")) != str:
        return {
            "result": "attribute `name` should be a string"
        }
    name = req["name"]
    mem, flag = loadDB(DB_JSON_NAME)
    if not flag:
        return {
            "result": "fail to open database file"
        }
    if mem.get(name) is None:
        mem[name] = [] # empty list
    values = mem[name]
    if req.get("maxn") is not None and type(req.get("maxn")) == int:
        maxn = req.get("maxn")
        if len(values) > maxn:
            values = values[-maxn:]
    return {
        "result": "read success",
        "data": values
    }

def getWriteData(req):
    assert type(req) == dict
    assert req.get("type") == "write"
    if req.get("name") is None or type(req.get("name")) != str:
        return {
            "result": "attribute `name` should be a string"
        }
    name = req["name"]
    if req.get("data") is None:
        return {
            "result": "attribute `data` should not be None"
        }
    data = req["data"]

    if req.get("hash") is None or type(req.get("hash")) != str:
        return {
            "result": "attribute `hash` should be a string"
        }
    if not checkHashCorrect(req):
        return {
            "result": "hash code incorrect"
        }

    mem, flag = loadDB(DB_JSON_NAME)
    if not flag:
        return {
            "result": "fail to open database file"
        }
    if mem.get(name) is None:
        mem[name] = [] # empty list
    if type(mem[name]) != list:
        return {
            "result": "inner error: mem[name] is not a list"
        }
    if data not in mem[name]:
        mem[name].append(data)
        if len(mem[name]) > MAX_VALUE_CNT:
            mem[name] = mem[name][-MAX_VALUE_CNT:]
        flag = saveDB(mem, DB_JSON_NAME)
        if not flag:
            return {
                "result": "fail to write database file"
            }
        return {
            "result": "write success"
        }
    else:
        return {
            "result": "value duplicated"
        }

def getOutputDataByInput(req):
    if type(req) != dict:
        return {
            "result": "request object must be a JSON object like dict"
        }
    if req.get("type") is None:
        return {
            "result": "request object must has a `type` attribute"
        }
    if req["type"] not in TYPE_LIST:
        return {
            "result": "`type` attribute must in TYPE_LIST = " + str(TYPE_LIST)
        }
    if req["type"] == "ping":
        return {
            "result": "connect to server successfully"
        }
    elif req["type"] == "read":
        return getReadData(req)
    elif req["type"] == "write":
        return getWriteData(req)
    else:
        return {
            "result": "inner error of GDSS"
        }

class Resquest(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get('content-length') is not None:
            try:
                datas = self.rfile.read(int(self.headers['content-length']))
                inputData = json.loads(datas.decode())
            except:
                inputData = {
                    "type": "ping"
                }
        else:
            inputData = {
                "type": "ping"
            }

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
