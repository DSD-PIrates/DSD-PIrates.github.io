import http.client
import json

SERVER_IP   = "139.155.89.85"
SERVER_PORT = 11451

def makeError(msg):
    return {"type"   : "Error", "message": str(msg)}

def clientRequest(data: dict, serverIP: str, serverPort: int):
    assert type(data)       == dict
    assert type(serverIP)   ==  str
    assert type(serverPort) ==  int
    conn = http.client.HTTPConnection("%s:%d" % (serverIP, serverPort))
    jsonData = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    try:
        conn.request("POST", "/", jsonData, headers)
        response = conn.getresponse()
        body = response.read().decode()
    except:
        body = None
    if body is None: return makeError("CanNotConnectToServer")
    # try to make it json
    try:    body = json.loads(body)
    except: body = None
    # return if it is json
    if body is not None: return body
    else:                return makeError("ServerResponseIsNotJson")

def Request_Raw(dataNow):
    ret = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
    print(json.dumps(ret, indent=4) + "\n")

# interfaces:

def Request_GetRealtimeData():
    Request_Raw({"type":"GetRealtimeData"})

def Request_GetSensorStatus():
    Request_Raw({"type":"GetSensorStatus"})

def Request_SensorCalibration():
    Request_Raw({"type":"SensorCalibration"})

def Request_GetSensorDetails():
    Request_Raw({"type":"GetSensorDetails"})

def Request_Ping():
    Request_Raw({"type":"Ping"})


if __name__ == "__main__":
    Request_GetRealtimeData  ()
    Request_GetSensorStatus  ()
    Request_SensorCalibration()
    Request_GetSensorDetails ()
    Request_Ping             ()