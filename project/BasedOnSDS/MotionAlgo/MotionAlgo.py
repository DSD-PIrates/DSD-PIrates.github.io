import time
import threading
import DataLoader

SENSOR             = ["L1", "L2", "L3", "R1", "R2", "R3"]
VALUE              = ["X", "Y", "Z", "accX", "accY", "accZ", "asX", "asY", "asZ"]
THRESHOLD          = 500
DEFAULT_TIME_SPAN  = 0.2
TIME_SEGMENT_CHECK = 3
FRAME_CNT_CHECK    = int(round(TIME_SEGMENT_CHECK / DEFAULT_TIME_SPAN))
THRES_RATIO        = 0.8

def checkMove(dic1, dic2) -> bool:
    return DataLoader.getDistanceFromDelta(dic1, dic2) >= THRESHOLD

def __checkBufMove(cntBuf: list) -> bool:
    return sum(cntBuf) / len(cntBuf) >= THRES_RATIO

MOTION_ALGO_RUN = True
def motionAlgo(getDictInterface, onStartCallBack, timeSpan = DEFAULT_TIME_SPAN):
    global MOTION_ALGO_RUN
    lastDic = getDictInterface()
    nowDic  = None
    cntBuf = []
    while MOTION_ALGO_RUN:
        nowDic = getDictInterface()
        # count available
        if checkMove(lastDic, nowDic): cntBuf.append(1)
        else:                          cntBuf.append(0)
        # pop front if buf is too large
        while len(cntBuf) > FRAME_CNT_CHECK: cntBuf = cntBuf[1:]
        if len(cntBuf) == FRAME_CNT_CHECK and __checkBufMove(cntBuf):
            onStartCallBack()
        time.sleep(timeSpan)

def stopMotionAlgo():
    MOTION_ALGO_RUN = False

def runMotionAlgo(__getDictInterface, __onStartCallBack):
    MOTION_ALGO_RUN = True
    mythread = threading.Thread(target=motionAlgo, args=(__getDictInterface, __onStartCallBack))
    mythread.start()

def getDemoDictInterface(filename):
    data = DataLoader.getData(filename)
    def __getDictInterface(posContainer = [-1]):
        posContainer[0] += 1
        posContainer[0] %= len(data)
        print(posContainer[0])
        return data[posContainer[0]]
    return __getDictInterface

def cli():
    interface = getDemoDictInterface("stande.json")
    def outputInterface(cntContainer = [0]):
        cntContainer[0] += 1
        print("on start %d" % cntContainer[0])
    runMotionAlgo(interface, outputInterface)

if __name__ == "__main__":
    cli()