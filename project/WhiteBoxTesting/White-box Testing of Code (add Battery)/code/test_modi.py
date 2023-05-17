# from unittest.mock import MagicMock, AsyncMock
# from forTest_ES import TmpSensorCollector
# from bleak import BleakClient
# from ES import SensorCollector
# import pytest


# # (3) Test SensorCollector.__init__(self, macAddr, name)
# @pytest.mark.parametrize('macAddr, name, COST_PER_LV', [
#     ("F2:02:E0:8D:B8:05", "R1", 12),
#     ("C4:39:0D:A9:91:89", "R2", 12)
# ])
# def test_init(macAddr, name, COST_PER_LV):
#     testClass = SensorCollector(macAddr, name)
#     assert testClass.macAddr == macAddr
#     assert testClass.name == name
#     assert testClass.battery.data["battery"]["COST_PER_LV"] == COST_PER_LV


# # (6) Test SensorCollector.__batteryCheck(self, client)
# @pytest.mark.parametrize('macAddr, name, level', [
#     ("F2:02:E0:8D:B8:05", "R1", 100)
# ])
# def test_SensorCollectorBatteryCheck(macAddr, name, level):
#     testClass = SensorCollector(macAddr, name)
#     assert testClass.getSensorStatus()["battery"] == level


# # (13) Test SensorCollector.__start_raw(self)
# @pytest.fixture
# def mock_client():
#     client = MagicMock(spec=BleakClient)
#     client.is_connected = AsyncMock(return_value=True)
#     client.read_gatt_char = AsyncMock(return_value=b'\x01\x02\x03')
#     return client


# @pytest.mark.asyncio
# async def test_my_function(mock_client):
#     async with mock_client as client:
#         # Call the function to be tested
#         tmp = TmpSensorCollector('00:11:22:33:44:55', 'My Device')

#         # 使用AsyncMock模拟BleakClient类和其方法
#         mock_client = AsyncMock()
#         mock_client.notification_handler = AsyncMock()
#         mock_client.read_gatt_char.return_value = b'\x01\x02\x03'
#         # mock_client.connect = AsyncMock(return_value=None)
#         mock_client.connect = AsyncMock()
#         mock_client.start_notify = AsyncMock()
#         mock_client.write_gatt_char = AsyncMock()
#         mock_client.disconnect = AsyncMock()
#         mock_client.is_connected.return_value = True
#         # mock_client.is_connected = AsyncMock(return_value=True)

#         # # 将模拟的BleakClient对象注入到MyClass实例中
#         # tmp._SensorCollector__client = client

#         await tmp._TmpSensorCollector__start_raw(client)
#         # Check the result
#         # assert result == expected_result
#         client.connect.assert_awaited_once()
#         client.start_notify.assert_awaited_once()
#         # client.start_notify.assert_awaited_once_with(IMU_READ_UUID, mock_client.notification_handler)
#         client.disconnect.assert_awaited_once()
#         client.write_gatt_char.assert_called()


# # (8) Test SensorCollector.getSensorStatus(self)
# @pytest.mark.parametrize('macAddr, name, expected_val', [
#     ("F2:02:E0:8D:B8:05", "R1", {"connect": False, "battery": 100})
# ])
# def test_getSensorStatus(macAddr, name, expected_val):
#     testClass = SensorCollector(macAddr, name)
#     assert testClass.getSensorStatus() == expected_val
