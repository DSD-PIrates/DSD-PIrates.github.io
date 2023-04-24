import http.client
import json
import time

ES_HOST_IP   = "127.0.0.1"
ES_HOST_PORT = 40096

def GetJsonData(es_ip: str, es_port: int, jsonData):
    headers = {
        "Content-type": "text/json"
    }
    conn = http.client.HTTPConnection("%s:%d" % (es_ip, es_port))
    conn.request("POST", "/", body=json.dumps(jsonData), headers=headers)
    response = conn.getresponse()
    dataRecv = json.loads(response.read())
    return dataRecv

if __name__ == "__main__":
    while True:
        testData = GetJsonData(ES_HOST_IP, ES_HOST_PORT, {"type": "GetRealtimeData"})
        print(testData)
        time.sleep(10)
