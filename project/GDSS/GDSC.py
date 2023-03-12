import requests
import json
import hashlib

SERVER_URL = "http://localhost:8192"
SERVER_PASSWORD = "GDSS-GGN-2015"

def getMd5(s: str):
    assert type(s) == str
    str_to_encode = s
    md5_obj = hashlib.md5()
    md5_obj.update(str_to_encode.encode('utf-8'))
    md5_code = md5_obj.hexdigest()
    return str(md5_code)

def sendRequest(url, data):
    try:
        data = json.dumps(data)
        suc_flag = True
    except:
        suc_flag = False
    if not suc_flag:
        return {
            "result": "client parser error"
        }
    try:
        res = requests.post(url=url,
                headers ={"Content-Type": "text/json; charset=utf-8"},
                data = data)
        ans = res.text
    except:
        ans = {
            "result": "connection failed"
        }
    return ans

def readDataFromServer(name, maxn):
    assert type(name) == str
    assert type(maxn) == int and maxn > 0

    ans = sendRequest(SERVER_URL, {
        "type": "read",
        "name": name,
        "maxn": maxn
    })
    return ans

def writeDataToServer(name, data):
    assert type(name) == str
    obj_tosend = {
        "type" : "write",
        "name": name,
        "data" : data,
        "hash" : SERVER_PASSWORD
    }
    hash_value = getMd5(json.dumps(obj_tosend))
    obj_tosend["hash"] = hash_value
    ans = sendRequest(SERVER_URL, obj_tosend)
    return ans

if __name__ == "__main__":
    print(writeDataToServer("sensor_l1_v1", {
        "value": "test"
    }))
