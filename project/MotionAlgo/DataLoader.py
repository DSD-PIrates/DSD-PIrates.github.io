import json
import os

DIRNAME   = os.path.dirname(__file__)
DATAPATH  = os.path.join(DIRNAME, "DATA")
SENSOR    = ["L1", "L2", "L3", "R1", "R2", "R3"]
VALUE     = ["X", "Y", "Z", "accX", "accY", "accZ", "asX", "asY", "asZ"]
THRESHOLD = 500

def getData(filename):
    filepath = os.path.join(DATAPATH, filename)
    return json.load(open(filepath))

def getDelta(dic1, dic2):
    ans = {}
    for tag in SENSOR: ans[tag] = {}
    for sensor in SENSOR:
        for value in VALUE:
            ans[sensor][value] = dic2[sensor][value] - dic1[sensor][value]
    return ans

def getDistanceFromDelta(dic1, dic2):
    ans = 0
    delta = getDelta(dic1, dic2)
    for sensor in SENSOR:
        for value in VALUE:
            ans += abs(delta[sensor][value])
    return ans

def getAvgDeltaFromFile(filename):
    data = getData(filename)
    assert len(data) >= 2 and type(data) == list
    ans = 0
    cnt = 0
    for i in range(1, len(data)):
        ans += getDistanceFromDelta(data[i-1], data[i])
        cnt += 1
    return ans / cnt

def getAvgForAllDataFile():
    for file in os.listdir(DATAPATH):
        print("%-15s DIS : %12.6lf" % (file, getAvgDeltaFromFile(file)))

def getThresAcc(filename, thres):
    data = getData(filename)
    assert len(data) >= 2 and type(data) == list
    ans = 0
    for i in range(1, len(data)):
        tmp = getDistanceFromDelta(data[i-1], data[i])
        if tmp > thres:
            ans += 1
    return ans / (len(data) - 1)

def getThresAccForAllDataFile(thres):
    for file in os.listdir(DATAPATH):
        print("%-15s DIS : %6.2lf %%" % (file, getThresAcc(file, thres)* 100))

getThresAccForAllDataFile(THRESHOLD)
