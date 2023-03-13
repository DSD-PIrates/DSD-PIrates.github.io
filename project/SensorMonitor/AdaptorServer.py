from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

import GDSC

host_ip = '0.0.0.0'
host = (host_ip, 8000)

last_send_time = {}

def pushValue(ans, nowStr):
    assert type(ans) == list
    assert type(nowStr) == str

    if nowStr == "%":
        ans.append(nowStr)
    else:
        tmp = chr(int(nowStr[1:], base=16))
        ans.append(tmp)

def processUnescape(encoded):
    assert type(encoded) == str
    ans = []
    nowStr = ""
    for x in list(encoded):
        if nowStr != "" and nowStr[0] == "%":  # has a % in nowStr
            if (ord("0") <= ord(x) <= ord("9")) or (ord("A") <= ord(x) <= ord("F")): # number
                nowStr += x
                if len(nowStr) == 3:
                    pushValue(ans, nowStr)
                    nowStr = ""
            elif x == "%":
                nowStr = ""
                ans.append("%")
            else:
                pushValue(ans, nowStr)
                nowStr = ""
                ans.append(x)
        elif x == "%":
            nowStr = "%"
        else:
            ans.append(x)
            nowStr = ""
    
    if nowStr != "" and nowStr[0] == "%":
        pushValue(ans, nowStr)
        nowStr = ""

    return "".join(ans)

def processDataToObject(encoded):
    assert type(encoded) == str
    unescaped = processUnescape(encoded)
    ans = {}
    for value in unescaped.split('&'):
        if value.find("=") != -1:
            left, right = value.split("=", 1)
            ans[left] = right
    return ans

def getDeviceNameWithVersion(deviceName):
    assert type(deviceName) == str
    assert deviceName.find("(") != -1
    return deviceName.split("(", 1)[0] + "_v" + GDSC.VERSION

MIN_SEGMENT = 0.2

def shouldSend(deviceName):
    global last_send_time
    assert type(last_send_time) == dict
    if last_send_time.get(deviceName) is None:
        last_send_time[deviceName] = time.time()
        return True
    else:
        timeNow = time.time()
        if timeNow - last_send_time[deviceName] > MIN_SEGMENT: # cache timeout
            last_send_time[deviceName] =  timeNow
            return True
        else:
            return False

def relaySendData(inputData):
    if type(inputData) != dict:
        return
    if inputData.get("deviceName") is None or type(inputData.get("deviceName")) != str:
        return
    copy_inputData = GDSC.deepCopy(inputData)
    deviceName = copy_inputData["deviceName"]
    deviceName = getDeviceNameWithVersion(deviceName)
    if shouldSend(deviceName):
        copy_inputData.pop("deviceName") # delete this attribute
        ans = GDSC.writeDataToServer(deviceName, copy_inputData)
    
class Resquest(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get('content-length') is not None:
            datas = self.rfile.read(int(self.headers['content-length']))
            # inputData = datas.decode()
            inputData = processDataToObject(datas.decode())
        else:
            inputData = {}

        relaySendData(inputData)
        data = {
            "result": "connect to PC successfully"
        }

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
