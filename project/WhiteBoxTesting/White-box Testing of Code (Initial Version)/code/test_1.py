from Plugin import f
import pytest
import datetime

# (1) Test Plugin.f(data:bytes)
@pytest.mark.parametrize('data, expected_val', [
    (b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
     {"X": 0, "Y": 0, "Z": 0, "accX": 0, "accY": 0, "accZ": 0, "asX": 0, "asY": 0, "asZ": 0})
])
def test_f(data, expected_val):
    returnValue = f(data)
    assert returnValue == expected_val