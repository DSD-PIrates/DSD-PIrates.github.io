import requests
import json
import hashlib

import Dumper

SERVER_URL = "http://139.155.89.85:8192"
SERVER_PASSWORD = "GDSS-GGN-2015"
VERSION = "0.0.1"

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

def readDataFromServer(name, maxn=1):
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
        "name": name,
        "type" : "write",
        "data" : data,
        "hash" : SERVER_PASSWORD
    }
    hash_value = getMd5(Dumper.MyDumps(obj_tosend))
    obj_tosend["hash"] = hash_value
    ans = sendRequest(SERVER_URL, obj_tosend)
    return ans

if __name__ == "__main__":
    ans = readDataFromServer("WT901-R3_v0.0.1")
    print(ans)
