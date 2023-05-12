import MotionAlgo.DataLoader as DataLoader
import MotionAlgo.MotionAlgo as MotionAlgo
from termcolor import colored

def __info(msg, status, ok: bool):
    print("%-40s " % msg, end = "")
    print(colored(status, "green" if ok else "red"))

SAMPLE_DATA=[{"R1":{"X":1,"Y":2,"Z":3,"accX":4,"accY":5,"accZ":6,"asX":7,"asY":8,"asZ":9},"R2":{"X":10,"Y":11,"Z":12,"accX":13,"accY":14,"accZ":15,"asX":16,"asY":17,"asZ":18},"R3":{"X":19,"Y":20,"Z":21,"accX":22,"accY":23,"accZ":24,"asX":25,"asY":26,"asZ":27},"L1":{"X":28,"Y":29,"Z":30,"accX":31,"accY":32,"accZ":33,"asX":34,"asY":35,"asZ":36},"L2":{"X":37,"Y":38,"Z":39,"accX":40,"accY":41,"accZ":42,"asX":43,"asY":44,"asZ":45},"L3":{"X":46,"Y":47,"Z":48,"accX":49,"accY":50,"accZ":51,"asX":52,"asY":53,"asZ":54},"timestamp":55},{"R1":{"X":55,"Y":54,"Z":53,"accX":52,"accY":51,"accZ":50,"asX":49,"asY":48,"asZ":47},"R2":{"X":46,"Y":45,"Z":44,"accX":43,"accY":42,"accZ":41,"asX":40,"asY":39,"asZ":38},"R3":{"X":37,"Y":36,"Z":35,"accX":34,"accY":33,"accZ":32,"asX":31,"asY":30,"asZ":29},"L1":{"X":28,"Y":27,"Z":26,"accX":25,"accY":24,"accZ":23,"asX":22,"asY":21,"asZ":20},"L2":{"X":19,"Y":18,"Z":17,"accX":16,"accY":15,"accZ":14,"asX":13,"asY":12,"asZ":11},"L3":{"X":10,"Y":9,"Z":8,"accX":7,"accY":6,"accZ":5,"asX":4,"asY":3,"asZ":2},"timestamp":1}]
SAMPLE_DELTA={'L1': {'X': 0, 'Y': -2, 'Z': -4, 'accX': -6, 'accY': -8, 'accZ': -10, 'asX': -12, 'asY': -14, 'asZ': -16}, 
'L2': {'X': -18, 'Y': -20, 'Z': -22, 'accX': -24, 'accY': -26, 'accZ': -28, 'asX': -30, 'asY': -32, 'asZ': -34}, 'L3': {'X': -36, 'Y': -38, 'Z': -40, 'accX': -42, 'accY': -44, 'accZ': -46, 'asX': -48, 'asY': -50, 'asZ': -52}, 'R1': {'X': 54, 'Y': 52, 'Z': 50, 'accX': 48, 'accY': 46, 'accZ': 44, 'asX': 42, 'asY': 40, 'asZ': 38}, 'R2': {'X': 36, 'Y': 34, 'Z': 32, 'accX': 30, 'accY': 28, 'accZ': 26, 'asX': 24, 'asY': 22, 'asZ': 20}, 'R3': {'X': 18, 'Y': 16, 'Z': 14, 'accX': 12, 'accY': 10, 'accZ': 8, 'asX': 6, 'asY': 4, 'asZ': 2}}

assert DataLoader.getData("sample.json") == SAMPLE_DATA
__info("DataLoader.getData", "[OK]", True)

lis = DataLoader.getData("sample.json")
assert DataLoader.getDelta(lis[0], lis[1]) == SAMPLE_DELTA
__info("DataLoader.getDelta", "[OK]", True)

assert DataLoader.getDistanceFromDelta(lis[0], lis[1]) == 1458
__info("DataLoader.getDistanceFromDelta", "[OK]", True)

assert DataLoader.getAvgDeltaFromFile("sample.json") == 1458.0
__info("DataLoader.getAvgDeltaFromFile", "[OK]", True)
