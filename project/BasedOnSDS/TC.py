import http.client
import json
import time
import os
import threading

ES_HOST_IP   = "127.0.0.1"
ES_HOST_PORT = 40096
DELTA_TIME   = 0.2 # sec

# 程序路径
# path = getCurDir()
def getCurDir():
    return os.path.dirname(__file__)

# 获得数据路径
def getDataDir():
    path = getCurDir()
    return os.path.join(path, "DATA")

# 数据路径
# dataFile = getFilePath(fileName)
def getFilePath(fileName):
    path = getDataDir()
    return os.path.join(path, fileName)

def GetJsonData(es_ip: str, es_port: int, jsonData):
    headers = {
        "Content-type": "text/json"
    }
    conn = http.client.HTTPConnection("%s:%d" % (es_ip, es_port))
    conn.request("POST", "/", body=json.dumps(jsonData), headers=headers)
    response = conn.getresponse()
    dataRecv = json.loads(response.read())
    return dataRecv

# 等待不超过一秒
def wait1():
    time.sleep(min(DELTA_TIME * 10, 1))

runFlag = False
programOn = True
cachedData = []
def collectData():
    while programOn:
        while runFlag == True:
            try:
                testData = GetJsonData(ES_HOST_IP, ES_HOST_PORT, {"type": "GetRealtimeData"})
            except:
                testData = None
            if testData is not None:
                cachedData.append(testData)
            time.sleep(DELTA_TIME)
        wait1()

def saveFile(cachedData, fileName):
    dataFile = getFilePath(fileName)
    with open(dataFile, "w") as fp:
        json.dump(cachedData, fp=fp)
    print("[*] save to file: %s" % fileName)

def cli():
    global runFlag
    global programOn
    global cachedData
    my_thread = threading.Thread(target=collectData)
    my_thread.start()
    while True:
        instruction = input(">>> ").strip()
        if instruction == "s": # 开始录制
            print("[+] record start ...")
            runFlag = True
        elif instruction == "e": # 结束录制
            print("[-] record end ...")
            runFlag = False
            wait1()
            print("[*] cachedData len = %d\n" % len(cachedData))
            fileName   = input("fileName(.json) >>> ").strip()
            if fileName.find(".json") == -1: # 补充后缀名
                fileName += ".json"
            saveFile(cachedData, fileName)
            cachedData = []
            wait1()
        elif instruction == "exit": # 退出程序
            print("[*] bye ...")
            break
    runFlag = False
    programOn = False

if __name__ == "__main__":
    cli()