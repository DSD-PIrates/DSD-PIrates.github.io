import http.client
import json

# DemoEmbeddedSystem: IP, Port
SERVER_IP   = "127.0.0.1"
SERVER_PORT = 40096

def makeError(msg):
    return {"type"   : "Error", "message": str(msg)}

# Send a JsonData HTTP-POST request to (serverIP, serverPort)
def clientRequest(data: dict, serverIP: str, serverPort: int):
    # assert type(data)       == dict
    # assert type(serverIP)   ==  str
    # assert type(serverPort) ==  int
    conn = http.client.HTTPConnection("%s:%d" % (serverIP, serverPort))
    jsonData = json.dumps(data)
    # jsonData = data
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
    
# "dataNow" is the JSON data to send, "ret" is the response from EmbeddedSystem
dataNow = {
    "name": "Test"
}
# dataNow = [1,2]
ret = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
print(ret)