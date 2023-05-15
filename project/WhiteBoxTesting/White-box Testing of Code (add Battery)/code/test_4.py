from ES import DataTransform
from ES import SensorCollector
from ES import Configuration
from ES import SensorStatus
from ES import SensorDetails
from ES import RealTimeData
from ES import SensorCalibration
from ES import Transaction
import pytest
import datetime
import ES
from forTest_ES import TmpSensorCollector
import forTest_ES
from unittest.mock import AsyncMock, MagicMock
from bleak import BleakClient


def sensorCollectorList():
    List = []
    List.append(SensorCollector("F2:02:E0:8D:B8:05", "R1"))
    List.append(SensorCollector("C4:39:0D:A9:91:89", "R2"))
    List.append(SensorCollector("E8:67:FE:A6:D4:3C", "R3"))
    List.append(SensorCollector("D1:7A:2A:54:02:95", "L1"))
    List.append(SensorCollector("D7:0F:4F:1D:4F:B5", "L2"))
    List.append(SensorCollector("E6:7A:B7:B0:45:9D", "L3"))
    return List

# (13) Test SensorCollector.__start_raw(self)
@pytest.fixture
def mock_client():
    client = MagicMock(spec=BleakClient)
    client.is_connected = AsyncMock(return_value=True)
    client.read_gatt_char = AsyncMock(return_value=b'\x01\x02\x03')
    return client


@pytest.mark.asyncio
async def test_my_function(mock_client):
    async with mock_client as client:
        # Call the function to be tested
        tmp = TmpSensorCollector('00:11:22:33:44:55', 'My Device')

        # Ê¹ÓÃAsyncMockÄ£ÄâBleakClientÀàºÍÆä·½·¨
        mock_client = AsyncMock()
        mock_client.notification_handler = AsyncMock()
        mock_client.read_gatt_char.return_value = b'\x01\x02\x03'
        # mock_client.connect = AsyncMock(return_value=None)
        mock_client.connect = AsyncMock()
        mock_client.start_notify = AsyncMock()
        mock_client.write_gatt_char = AsyncMock()
        mock_client.disconnect = AsyncMock()
        mock_client.is_connected.return_value = True
        # mock_client.is_connected = AsyncMock(return_value=True)

        # # ½«Ä£ÄâµÄBleakClient¶ÔÏó×¢Èëµ½MyClassÊµÀýÖÐ
        # tmp._SensorCollector__client = client

        await tmp._TmpSensorCollector__start_raw(client)
        # Check the result
        # assert result == expected_result
        client.connect.assert_awaited_once()
        client.start_notify.assert_awaited_once()
        # client.start_notify.assert_awaited_once_with(IMU_READ_UUID, mock_client.notification_handler)
        client.disconnect.assert_awaited_once()
        client.write_gatt_char.assert_called()




# (14) Test Configuration.getMacAddrOfSensor(self, index)
@pytest.mark.parametrize('data, expected_val', [
    (0, "F2:02:E0:8D:B8:05"),
    (1, "C4:39:0D:A9:91:89")
])
def test_getMacAddrOfSensor(data, expected_val):
    testClass = ES.Configuration()
    Mac = testClass.getMacAddrOfSensor(data)
    assert Mac == expected_val




# (15) Test Configuration.getNameOfSensor(self, index)
@pytest.mark.parametrize('data, expected_val', [
    (0, "R1"),
    (1, "R2")
])
def test_getNameOfSensor(data, expected_val):
    testClass = ES.Configuration()
    name = testClass.getNameOfSensor(data)
    assert name == expected_val




# (16) Test SensorStatus.__init__(self, sensorCollectorList)
@pytest.mark.parametrize('data', [
    (sensorCollectorList())
])
def test_SensorStatusInit(data):
    SensorStatus(data)
    assert True


# (17) Test Configuration.getJsonObject(self)
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
def test_getJsonObject(data):
    testClass = Configuration()
    assert testClass.getJsonObject() == data




# (18) Test Transaction.getResponse(self, dataInput)
def test_TransactionGetResponse():
    transaction = Transaction(sensorCollectorList())
    assert transaction.getResponse({"name": "test", "macAddr":  "test"}) == ES.ERROR_MESSAGE






# (19) Test SensorDetails.__init__(self, sensorCollectorList)
@pytest.mark.parametrize('data', [
    (sensorCollectorList())
])
def test_SensorDetailsInit(data):
    testClass = SensorDetails(data, Configuration())
    assert type(testClass.config) == Configuration


# (20) Test SensorCalibration.__init__(self, sensorCollectorList)
@pytest.mark.parametrize('data', [
    (sensorCollectorList())
])
def test_SensorCalibrationInit(data):
    SensorCalibration(data)
    assert True



# (21) Test RealTimeData.__init__(self, sensorCollectorList)
@pytest.mark.parametrize('data', [
    (sensorCollectorList())
])
def test_RealTimeDataInit(data):
    RealTimeData(data)
    assert True


# (22) Test Transaction.checkSuitable(self, dataInput)
def test_TransactionCheckSuitable():
    transaction = Transaction(sensorCollectorList())
    assert transaction.checkSuitable({"name": "test", "macAddr":  "test"}) == False


# (8) Test SensorCollector.getSensorStatus(self)
@pytest.mark.parametrize('macAddr, name, expected_val', [
    ("F2:02:E0:8D:B8:05", "R1", {"connect": False, "battery": 100})
])
def test_getSensorStatus(macAddr, name, expected_val):
    testClass = SensorCollector(macAddr, name)
    assert testClass.getSensorStatus() == expected_val
