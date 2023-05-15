from ES import DataTransform
from ES import SensorCollector
import pytest



# (2) Test DataTransform.transform(self, data)
@pytest.mark.parametrize('data, expected_val', [
    (b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
     {"X": 0, "Y": 0, "Z": 0, "accX": 0, "accY": 0, "accZ": 0, "asX": 0, "asY": 0, "asZ": 0})
])
def test_transform(data, expected_val):
    testClass = DataTransform()
    assert testClass.transform(data) == expected_val




# Test SensorCollector.__init__(self, macAddr, name)
@pytest.mark.parametrize('macAddr, name', [
    ("F2:02:E0:8D:B8:05", "R1"),
    ("C4:39:0D:A9:91:89", "R2")
])

def test_init(macAddr, name):
    testClass = SensorCollector(macAddr, name)
    assert testClass.macAddr == macAddr
    assert testClass.name == name