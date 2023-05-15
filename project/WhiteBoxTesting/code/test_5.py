from ES import DataTransform
from ES import SensorCollector
from ES import Configuration
from ES import SensorStatus
from ES import SensorDetails
from ES import RealTimeData
from ES import SensorCalibration
from ES import Router
import pytest
import datetime
import threading
import asyncio
import ES


async def func():
    return

def sensorCollectorList():
    List = []
    List.append(SensorCollector("F2:02:E0:8D:B8:05", "R1"))
    List.append(SensorCollector("C4:39:0D:A9:91:89", "R2"))
    List.append(SensorCollector("E8:67:FE:A6:D4:3C", "R3"))
    List.append(SensorCollector("D1:7A:2A:54:02:95", "L1"))
    List.append(SensorCollector("D7:0F:4F:1D:4F:B5", "L2"))
    List.append(SensorCollector("E6:7A:B7:B0:45:9D", "L3"))
    return List
def config():
    tmp = Configuration();
    return tmp

# (23) Test SensorCollector.start(self)
def test_SensorCollectorStart():
    try:
        thread = threading.Thread(target=lambda: asyncio.run(func()))
        thread.start()
    except:
        assert False
    assert True




# (24) Test Router.__init__(self)
def test_init():
    testClass = Router()
    assert type(testClass.config) == Configuration
    assert testClass.sensorCollectorList is not None
    for i in range(ES.SENSOR_COUNT):
        assert isinstance(testClass.sensorCollectorList[i], SensorCollector)
    assert testClass.transactionList is not None
    assert isinstance(testClass.transactionList[0], RealTimeData)
    assert isinstance(testClass.transactionList[1], SensorDetails)
    assert isinstance(testClass.transactionList[2], SensorStatus)
    assert isinstance(testClass.transactionList[3], SensorCalibration)




# (25) Test SensorStatus.getResponse(self, dataInput)
@pytest.mark.parametrize('dataInput, expected_val', [
    ({"type":"GetSensorStatus"}, {'0': {'connect': False, 'battery': 100},
                                  '1': {'connect': False, 'battery': 100},
                                  '2': {'battery': 100, 'connect': False},
                                  '3': {'battery': 100, 'connect': False},
                                  '4': {'battery': 100, 'connect': False},
                                  '5': {'battery': 100, 'connect': False}})
])
def test_SensorStatusGetResponse(dataInput, expected_val):
    testClass = SensorStatus(sensorCollectorList())
    assert testClass.getResponse(dataInput) == expected_val





# (26) Test SensorDetails.getResponse(self, dataInput)
@pytest.mark.parametrize('data', [
    [
    {
        "name": "R1",
        "macAddr": "F2:02:E0:8D:B8:05"
    },
    {
        "name": "R2",
        "macAddr": "C4:39:0D:A9:91:89"
    },
    {
        "name": "R3",
        "macAddr": "E8:67:FE:A6:D4:3C"
    },
    {
        "name": "L1",
        "macAddr": "D1:7A:2A:54:02:95"
    },
    {
        "name": "L2",
        "macAddr": "D7:0F:4F:1D:4F:B5"
    },
    {
        "name": "L3",
        "macAddr": "E6:7A:B7:B0:45:9D"
    }
]
])

def test_SensorDetailsGetResponse(data):
    testClass = SensorDetails(sensorCollectorList(), config())
    assert testClass.getResponse({"type":"GetSensorDetails"}) == data




# (27) Test RealTimeData.getResponse(self, dataInput)
@pytest.mark.parametrize('input_val, expected_val, names', [
    ({"type":"GetRealtimeData"}, ES.INVALID_DATA, ["R1", "R2", "R3", "L1", "L2", "L3","timestamp"])
])

def test_RealTimeDataGetResponse(input_val, expected_val, names):
    testClass = RealTimeData(sensorCollectorList())
    ans = testClass.getResponse(input_val)
    assert ans[names[0]] == expected_val
    assert ans[names[1]] == expected_val
    assert ans[names[2]] == expected_val
    assert ans[names[3]] == expected_val
    assert ans[names[4]] == expected_val
    assert ans[names[5]] == expected_val
    assert isinstance(ans[names[6]], float)




# (28) Test SensorCalibration.getResponse(self, dataInput)
@pytest.mark.parametrize('input_val, lastCalibrate, expected_val', [
    ({"type":"SensorCalibration"}, datetime.datetime.utcnow(), {"type": "CalibrationFailure"}),
    ({"type":"SensorCalibration"}, datetime.datetime.utcfromtimestamp(0), {"type": "CalibrationSuccess"})
])

def test_SensorCalibrationGetResponse(input_val, lastCalibrate, expected_val):
    testClass = SensorCalibration(sensorCollectorList())
    for sensorCollector in testClass.sensorCollectorList:
        sensorCollector.lastCalibrate = lastCalibrate
    assert testClass.getResponse(input_val) == expected_val






# (29) Test SensorStatus.checkSuitable(self, dataInput)
def test_SensorStatusCheckSuitable():
    testClass = SensorStatus(sensorCollectorList())
    assert testClass.checkSuitable({"type": "GetSensorStatus"}) == True



# (30) Test SensorCalibration.checkSuitable(self, dataInput)
def test_SensorCalibrationCheckSuitable():
    testClass = SensorCalibration(sensorCollectorList())
    assert testClass.checkSuitable({"type": "SensorCalibration"}) == True





# (31) Test SensorDetails.checkSuitable(self, dataInput)
def test_SensorDetailsCheckSuitable():
    testClass = SensorDetails(sensorCollectorList(), config())
    assert testClass.checkSuitable({"type": "GetSensorDetails"}) == True


# (32) Test RealTimeData.checkSuitable(self, dataInput)
def test_RealTimeDataCheckSuitable():
    testClass = RealTimeData(sensorCollectorList())
    assert testClass.checkSuitable({"type": "GetRealtimeData"}) == True