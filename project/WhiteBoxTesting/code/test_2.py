from ES import DataTransform
from ES import SensorCollector
import pytest
from ES import Battery



# (2) Test DataTransform.transform(self, data)
@pytest.mark.parametrize('data, expected_val', [
    (b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
     {"X": 0, "Y": 0, "Z": 0, "accX": 0, "accY": 0, "accZ": 0, "asX": 0, "asY": 0, "asZ": 0})
])
def test_transform(data, expected_val):
    testClass = DataTransform()
    assert testClass.transform(data) == expected_val




# (3) Test SensorCollector.__init__(self, macAddr, name)
# @pytest.mark.parametrize('macAddr, name', [
#     ("F2:02:E0:8D:B8:05", "R1"),
#     ("C4:39:0D:A9:91:89", "R2")
# ])

# def test_init(macAddr, name):
#     testClass = SensorCollector(macAddr, name)
#     assert testClass.macAddr == macAddr
#     assert testClass.name == name


# (37) Test Battery.__init__(self)
def test_singleton():
    assert Battery() is Battery()
def test_battery_initial_level():
    # 读取初始电量
    battery = Battery()
    initial_level = battery.batterycheck()
    assert initial_level == 100