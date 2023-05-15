import pytest
import DataLoader as DL
import MotionAlgo as MA

SAMPLE_DATA = [{"R1": {"X": 1, "Y": 2, "Z": 3, "accX": 4, "accY": 5, "accZ": 6, "asX": 7, "asY": 8, "asZ": 9},
                "R2": {"X": 10, "Y": 11, "Z": 12, "accX": 13, "accY": 14, "accZ": 15, "asX": 16, "asY": 17, "asZ": 18},
                "R3": {"X": 19, "Y": 20, "Z": 21, "accX": 22, "accY": 23, "accZ": 24, "asX": 25, "asY": 26, "asZ": 27},
                "L1": {"X": 28, "Y": 29, "Z": 30, "accX": 31, "accY": 32, "accZ": 33, "asX": 34, "asY": 35, "asZ": 36},
                "L2": {"X": 37, "Y": 38, "Z": 39, "accX": 40, "accY": 41, "accZ": 42, "asX": 43, "asY": 44, "asZ": 45},
                "L3": {"X": 46, "Y": 47, "Z": 48, "accX": 49, "accY": 50, "accZ": 51, "asX": 52, "asY": 53, "asZ": 54},
                "timestamp": 55},
               {"R1": {"X": 55, "Y": 54, "Z": 53, "accX": 52, "accY": 51, "accZ": 50, "asX": 49, "asY": 48, "asZ": 47},
                "R2": {"X": 46, "Y": 45, "Z": 44, "accX": 43, "accY": 42, "accZ": 41, "asX": 40, "asY": 39, "asZ": 38},
                "R3": {"X": 37, "Y": 36, "Z": 35, "accX": 34, "accY": 33, "accZ": 32, "asX": 31, "asY": 30, "asZ": 29},
                "L1": {"X": 28, "Y": 27, "Z": 26, "accX": 25, "accY": 24, "accZ": 23, "asX": 22, "asY": 21, "asZ": 20},
                "L2": {"X": 19, "Y": 18, "Z": 17, "accX": 16, "accY": 15, "accZ": 14, "asX": 13, "asY": 12, "asZ": 11},
                "L3": {"X": 10, "Y": 9, "Z": 8, "accX": 7, "accY": 6, "accZ": 5, "asX": 4, "asY": 3, "asZ": 2},
                "timestamp": 1}]
SAMPLE_DELTA = {
    'L1': {'X': 0, 'Y': -2, 'Z': -4, 'accX': -6, 'accY': -8, 'accZ': -10, 'asX': -12, 'asY': -14, 'asZ': -16},
    'L2': {'X': -18, 'Y': -20, 'Z': -22, 'accX': -24, 'accY': -26, 'accZ': -28, 'asX': -30, 'asY': -32, 'asZ': -34},
    'L3': {'X': -36, 'Y': -38, 'Z': -40, 'accX': -42, 'accY': -44, 'accZ': -46, 'asX': -48, 'asY': -50, 'asZ': -52},
    'R1': {'X': 54, 'Y': 52, 'Z': 50, 'accX': 48, 'accY': 46, 'accZ': 44, 'asX': 42, 'asY': 40, 'asZ': 38},
    'R2': {'X': 36, 'Y': 34, 'Z': 32, 'accX': 30, 'accY': 28, 'accZ': 26, 'asX': 24, 'asY': 22, 'asZ': 20},
    'R3': {'X': 18, 'Y': 16, 'Z': 14, 'accX': 12, 'accY': 10, 'accZ': 8, 'asX': 6, 'asY': 4, 'asZ': 2}
}


def getDictInterface(posContainer=[-1]):
    data = DL.getData('sample.json')
    posContainer[0] += 1
    posContainer[0] %= len(data)
    print(posContainer[0])
    return data[posContainer[0]]


def onStartCallBack():
    MA.MOTION_ALGO_RUN = False


# (1) Test getData(filename)
def test_checkMove():
    assert DL.getData("sample.json") == SAMPLE_DATA


# (2) Test getDelta(dic1, dic2)
def test_getDelta():
    lis = DL.getData("sample.json")
    assert DL.getDelta(lis[0], lis[1]) == SAMPLE_DELTA


# (3) Test getDistanceFromDelta(dic1, dic2)
def getDistanceFromDelta():
    lis = DL.getData("sample.json")
    assert DL.getDistanceFromDelta(lis[0], lis[1]) == 1458


# (4) Test getAvgDeltaFromFile(filename)
def test_getAvgDeltaFromFile():
    assert DL.getAvgDeltaFromFile("sample.json") == 1458.0


# (5) Test getAvgForAllDataFile()
def test_getAvgForAllDataFile():
    DL.getAvgForAllDataFile()


# (6) Test getThresAcc(filename, thres)
@pytest.mark.parametrize('thres, expected_acc', [
    (0, 1),
    (1500, 0)
])
def test_getThresAcc(thres, expected_acc):
    acc = DL.getThresAcc("sample.json", thres)
    assert acc == expected_acc


# (7) Test getThresAccForAllDataFile(thres)
def getThresAccForAllDataFile():
    DL.getThresAccForAllDataFile(0)


# (8) Test checkMove(dic1, dic2)
@pytest.mark.parametrize('data, expected_val', [
    ([{"R1": {"X": 1, "Y": 2, "Z": 3, "accX": 4, "accY": 5, "accZ": 6, "asX": 7, "asY": 8, "asZ": 9},
       "R2": {"X": 10, "Y": 11, "Z": 12, "accX": 13, "accY": 14, "accZ": 15, "asX": 16, "asY": 17, "asZ": 18},
       "R3": {"X": 19, "Y": 20, "Z": 21, "accX": 22, "accY": 23, "accZ": 24, "asX": 25, "asY": 26, "asZ": 27},
       "L1": {"X": 28, "Y": 29, "Z": 30, "accX": 31, "accY": 32, "accZ": 33, "asX": 34, "asY": 35, "asZ": 36},
       "L2": {"X": 37, "Y": 38, "Z": 39, "accX": 40, "accY": 41, "accZ": 42, "asX": 43, "asY": 44, "asZ": 45},
       "L3": {"X": 46, "Y": 47, "Z": 48, "accX": 49, "accY": 50, "accZ": 51, "asX": 52, "asY": 53, "asZ": 54},
       "timestamp": 55},
      {"R1": {"X": 55, "Y": 54, "Z": 53, "accX": 52, "accY": 51, "accZ": 50, "asX": 49, "asY": 48, "asZ": 47},
       "R2": {"X": 46, "Y": 45, "Z": 44, "accX": 43, "accY": 42, "accZ": 41, "asX": 40, "asY": 39, "asZ": 38},
       "R3": {"X": 37, "Y": 36, "Z": 35, "accX": 34, "accY": 33, "accZ": 32, "asX": 31, "asY": 30, "asZ": 29},
       "L1": {"X": 28, "Y": 27, "Z": 26, "accX": 25, "accY": 24, "accZ": 23, "asX": 22, "asY": 21, "asZ": 20},
       "L2": {"X": 19, "Y": 18, "Z": 17, "accX": 16, "accY": 15, "accZ": 14, "asX": 13, "asY": 12, "asZ": 11},
       "L3": {"X": 10, "Y": 9, "Z": 8, "accX": 7, "accY": 6, "accZ": 5, "asX": 4, "asY": 3, "asZ": 2},
       "timestamp": 1}], True),
    ([{"R1": {"X": 55, "Y": 54, "Z": 53, "accX": 52, "accY": 51, "accZ": 50, "asX": 49, "asY": 48, "asZ": 47},
       "R2": {"X": 46, "Y": 45, "Z": 44, "accX": 43, "accY": 42, "accZ": 41, "asX": 40, "asY": 39, "asZ": 38},
       "R3": {"X": 37, "Y": 36, "Z": 35, "accX": 34, "accY": 33, "accZ": 32, "asX": 31, "asY": 30, "asZ": 29},
       "L1": {"X": 56, "Y": 27, "Z": 26, "accX": 25, "accY": 24, "accZ": 23, "asX": 22, "asY": 21, "asZ": 20},
       "L2": {"X": 19, "Y": 18, "Z": 17, "accX": 16, "accY": 15, "accZ": 14, "asX": 13, "asY": 12, "asZ": 11},
       "L3": {"X": 22, "Y": 9, "Z": 8, "accX": 7, "accY": 6, "accZ": 5, "asX": 4, "asY": 3, "asZ": 2},
       "timestamp": 50},
      {"R1": {"X": 55, "Y": 54, "Z": 53, "accX": 52, "accY": 51, "accZ": 50, "asX": 49, "asY": 48, "asZ": 47},
       "R2": {"X": 46, "Y": 45, "Z": 44, "accX": 43, "accY": 42, "accZ": 41, "asX": 40, "asY": 39, "asZ": 38},
       "R3": {"X": 37, "Y": 36, "Z": 35, "accX": 34, "accY": 33, "accZ": 32, "asX": 31, "asY": 30, "asZ": 29},
       "L1": {"X": 28, "Y": 27, "Z": 26, "accX": 25, "accY": 24, "accZ": 23, "asX": 22, "asY": 21, "asZ": 20},
       "L2": {"X": 19, "Y": 18, "Z": 17, "accX": 16, "accY": 15, "accZ": 14, "asX": 13, "asY": 12, "asZ": 11},
       "L3": {"X": 10, "Y": 9, "Z": 8, "accX": 7, "accY": 6, "accZ": 5, "asX": 4, "asY": 3, "asZ": 2},
       "timestamp": 1}], False)
])
def test_checkMove(data, expected_val):
    val = MA.checkMove(data[0], data[1])
    assert val == expected_val


# (9) Test __checkBufMove(cntBuf: list)
@pytest.mark.parametrize('data, expected_val', [
    ([0.8, 0.7, 0.9, 0.6], True),
    ([0.5, 0.6, 0.3, 0.6], False),
])
def test_checkBufMove(data, expected_val):
    val = MA.__checkBufMove(data)
    assert val == expected_val


# (10) Test getDemoDictInterface(filename)
def test_getDemoDictInterface():
    assert MA.getDemoDictInterface('sample.json')() == SAMPLE_DATA[0]


# (11) Test motionAlgo(getDictInterface, onStartCallBack, timeSpan=DEFAULT_TIME_SPAN)
def test_motionAlgo():
    MA.THRES_RATIO = 0.4
    MA.motionAlgo(getDictInterface, onStartCallBack)
    assert not MA.MOTION_ALGO_RUN


# (12) Test runMotionAlgo(__getDictInterface, __onStartCallBack)
def test_runMotionAlgo():
    MA.THRES_RATIO = 0.4
    MA.runMotionAlgo(getDictInterface, onStartCallBack)


# (13) Test stopMotionAlgo()
def test_stopMotionAlgo():
    MA.stopMotionAlgo()
    assert not MA.MOTION_ALGO_RUN


# (14) Test cli()
def test_cli():
    MA.cli()
    MA.MOTION_ALGO_RUN = False
