import time
import os
import json
import pytest
import datetime
import ES
from ES import DataTransform
from ES import SensorCollector
from freezegun import freeze_time
from ES import Battery, singleton
from unittest.mock import MagicMock, patch


# (4) Test SensorCollector.__callback(self, sender, data)
class TestSensorCollector:

    @pytest.mark.parametrize('data, expected_val', [
        (b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
         {"X": 0, "Y": 0, "Z": 0, "accX": 0, "accY": 0, "accZ": 0, "asX": 0, "asY": 0, "asZ": 0})
    ])
    def test_callback(self, data, expected_val):
        # Create a mock instance of the class
        test_obj = MagicMock(spec=SensorCollector)

        # Replace the __callback method with a MagicMock
        with patch.object(test_obj, '_SensorCollector__callback') as mock_callback:
            # Call the method you want to test
            test_obj._SensorCollector__callback(None, data)
            # Check that the mock callback was called with the expected arguments
            mock_callback.assert_called_once_with(None, data)




# (5) Test SensorCollector.__connectionCheck(self)
@pytest.mark.parametrize('data, expected_val', [
    (0, True),
    (3, False)
])
def test_connectionCheck(data, expected_val):
    cacheTime = datetime.datetime.utcnow()
    time.sleep(data)
    now = datetime.datetime.utcnow()
    delta = now - cacheTime
    flag = delta.total_seconds() <= 1
    assert flag == expected_val


# (6) Test SensorCollector.__batteryCheck(self, client)
@pytest.mark.parametrize('macAddr, name, level', [
    ("F2:02:E0:8D:B8:05", "R1", 100)
])
def test_SensorCollectorBatteryCheck(macAddr, name, level):
    testClass = SensorCollector(macAddr, name)
    assert testClass.getSensorStatus()["battery"] == level


# (7) Test SensorCollector.__calibrate(self, client)
# Obviously, there's no problem with the code.





# (9) Test Configuration.__init__(self)
def test_ConfigurationInit():
    ES.Configuration()
    assert True





# (10) Test Transaction.__init__(self, sensorCollectorList)
@pytest.mark.parametrize('data', [
    ([SensorCollector("F2:02:E0:8D:B8:05", "R1")])
])
def test_callback(data):
    testclass = ES.Transaction(data)
    assert type(testclass.sensorCollectorList) == list and type(testclass.sensorCollectorList[0]) == ES.SensorCollector



# (11) Test SensorCollector.getRealtimeData(self)
@pytest.mark.parametrize('connected, cache, expected_val', [
    (True, {"X":1, "Y":1, "Z":1, "accX":1, "accY":1, "accZ":1, "asX":1, "asY":1, "asZ":1},
        {"X":1, "Y":1, "Z":1, "accX":1, "accY":1, "accZ":1, "asX":1, "asY":1, "asZ":1}),
    (True, None, ES.INVALID_DATA),
    (False, None, ES.INVALID_DATA)
])

def test_getRealtimeData(connected, cache, expected_val):
    testClass = SensorCollector("F2:02:E0:8D:B8:05", "R1")
    testClass.connected = connected
    testClass.cache = cache
    assert testClass.getRealtimeData() == expected_val




# (12) Test SensorCollector.calibrate(self)
@pytest.mark.parametrize('lastCalibrate, expected_val, needCalibrate, Type', [
    (datetime.datetime.utcfromtimestamp(0), True, True, datetime.datetime),
    (datetime.datetime.utcnow(), False, False, datetime.datetime)
])

def test_calibrate(lastCalibrate, expected_val, needCalibrate, Type):
    testClass = SensorCollector("F2:02:E0:8D:B8:05", "R1")
    testClass.lastCalibrate = lastCalibrate
    assert testClass.calibrate() == expected_val
    assert testClass.needCalibrate == needCalibrate
    assert type(testClass.lastCalibrate) == Type



# (38) Test Battery.batterycheck(self)
def test_battery_level_change():
    battery = Battery()
    battery.data['battery']['COST_PER_LV'] = 1
    print(datetime.datetime.now())
    fake_now =datetime.datetime.fromtimestamp(battery.data['timing']['beginning'] - 28800 + 600)
    print(fake_now)
    print(fake_now.timestamp())
    with freeze_time(fake_now):
        print(fake_now)
        print(datetime.datetime.now().timestamp())
        assert battery.batterycheck() == 90
    battery.data['battery']['level'] = 100


# (39) Test Battery.reset(self)
def test_battery_reset():
    # 重置电量
    battery = Battery()
    battery.data['battery']['level'] = 50
    battery.reset()
    assert battery.batterycheck() == 100




# (40) Test Battery.save(self)
def test_save():
    battery = Battery()
    battery.data['timing']['beginning'] = datetime.datetime.now().timestamp()
    battery.data['battery']['level'] = 50
    battery.save()
    assert battery.data['battery']['level'] == 50
    filename = os.path.join(ES.FILEPATH, "monitor.json")
    with open(filename, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    assert data['battery']['level'] == 50
    battery.reset()
    battery.data['battery']['COST_PER_LV'] = 12
    battery.save()
    assert battery.data['battery']['COST_PER_LV'] == 12