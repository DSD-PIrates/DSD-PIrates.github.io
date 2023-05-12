import http.client
import json
import time
import os
import threading
import MotionAlgo.MotionAlgo as MotionAlgo

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

def GetInternetData() -> dict:
    try:
        testData = GetJsonData(ES_HOST_IP, ES_HOST_PORT, {"type": "GetRealtimeData"})
    except:
        testData = None
    return testData

# 等待不超过一秒
def wait1():
    time.sleep(min(DELTA_TIME * 10, 1))

runFlag = False
programOn = True
cachedData = []
def collectData():
    while programOn:
        while runFlag == True:
            testData = GetInternetData()
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
        if instruction == "s": # start
            if not runFlag and not MotionAlgo.MOTION_ALGO_RUN:
                print("[+] record start ...")
                runFlag = True
            else:
                print("[!] error: started ")
        if instruction == "a": # auto start
            def __beginToRecord():
                global runFlag
                if not runFlag:
                    runFlag = True
                    print("[*] record auto start ...")
            if not runFlag and not MotionAlgo.MOTION_ALGO_RUN:        
                print("[+] waiting for  auto start ...")
                MotionAlgo.runMotionAlgo(GetInternetData, __beginToRecord)
            else:
                print("[!] error: started ")
            wait1()
        elif instruction == "e": # end
            print("[-] record end ...")
            runFlag = False
            MotionAlgo.stopMotionAlgo()
            wait1()
            print("[*] cachedData len = %d" % len(cachedData))
            fileName   = input("fileName(.json) >>> ").strip()
            if fileName != "":
                if fileName.find(".json") == -1: # 补充后缀名
                    fileName += ".json"
                saveFile(cachedData, fileName)
            else:
                print("[!] data discard")
            cachedData = []
            wait1()
        elif instruction == "exit": # 退出程序
            print("[*] bye ...")
            break
    runFlag   = False
    programOn = False
    MotionAlgo.stopMotionAlgo()

if __name__ == "__main__":
    cli()