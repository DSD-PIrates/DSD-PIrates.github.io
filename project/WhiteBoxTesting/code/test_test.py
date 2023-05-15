# import pytest
# import time
# import os
# import json
# import datetime
# from pytest_mock import mocker
# from ES import Battery, singleton
# import ES
# from unittest.mock import patch
# from freezegun import freeze_time
# #
# #
# #
# #
# #

# def test_singleton():
#     assert Battery() is Battery()

# def test_battery_initial_level():
#     # 读取初始电量
#     battery = Battery()
#     initial_level = battery.batterycheck()
#     assert initial_level == 100
# #
# #
# #
# def test_battery_level_change():
#     battery = Battery()
#     print(datetime.datetime.now())
#     fake_now =datetime.datetime.fromtimestamp(battery.data['timing']['beginning'] - 28800 + 600)
#     print(fake_now)
#     print(fake_now.timestamp())
#     with freeze_time(fake_now):
#         print(fake_now)
#         print(datetime.datetime.now().timestamp())
#         assert battery.batterycheck() == 90
#     # 等待一段时间，检查电量变化
#     # battery = Battery()
#     # initial_level = battery.batterycheck()
#     # time.sleep(2)
#     # level_1 = battery.batterycheck()
#     # assert level_1 < initial_level
#     # assert level_1 > 0
# #
# #
# # def test_battery_after_one_hour(mocker):
# #     # 模拟时间流逝1小时
# #     mocker.patch("datetime.datetime.now", lambda: datetime.datetime.now() + datetime.timedelta(hours=1))
# #
# #     # 测试电量是否下降
# #     battery = Battery()
# #     initial_level = battery.batterycheck()
# #     level_1 = battery.batterycheck()
# #     assert level_1 < initial_level
# #
# # def fake_datetime_now():
# #     return datetime.datetime(2023, 5, 15, hour=1)  # 返回固定的时间
# #
# #
# # def test_battery_after_one_hour():
# #     with patch("datetime.datetime.now", fake_datetime_now):
# #         # 测试代码
# #         # 测试电量是否下降
# #         battery = Battery()
# #         initial_level = battery.batterycheck()
# #         level_1 = battery.batterycheck()
# #         assert level_1 < initial_level
# #
# #
# #
# #
# #
# def test_battery_reset():
#     # 重置电量
#     battery = Battery()
#     battery.data['battery']['level'] = 50
#     battery.reset()
#     assert battery.batterycheck() == 100


# def test_save():
#     # 创建一个 Battery 对象
#     battery = Battery()

#     # 设置开始时间为当前时间
#     battery.data['timing']['beginning'] = datetime.datetime.now().timestamp()

#     # 设置电量为 50%
#     battery.data['battery']['level'] = 50

#     # 保存 Battery 对象
#     battery.save()

#     # 检查电量是否正确
#     assert battery.data['battery']['level'] == 50

#     # 检查保存后文件是否被正确更新
#     filename = os.path.join(ES.FILEPATH, "monitor.json")
#     with open(filename, "r", encoding="utf-8") as fp:
#         data = json.load(fp)
#     assert data['battery']['level'] == 50
#     battery.reset()
#     battery.save()
# #
# # def test_battery_level_difference():
# #     # 检查电量变化是否正确
# #     battery = Battery()
# #     initial_level = battery.batterycheck()
# #     time.sleep(2)
# #     level_1 = battery.batterycheck()
# #     time.sleep(2)
# #     level_2 = battery.batterycheck()
# #     assert level_1 != level_2
# #     assert level_1 > level_2 > 0
# #
# #
# #
# # # import os
# # # import json
# # # from datetime import datetime
# # # from unittest.mock import patch, MagicMock
# # # import pytest
# # #
# # # from ES import singleton, Battery
# # #
# # #
# # # @pytest.fixture
# # # def battery():
# # #     return Battery()
# # #
# # #
# # # class TestBattery:
# # #     def setUp(self):
# # #         self.filepath = os.path.join(os.path.dirname(__file__), "monitor.json")
# # #
# # #     @patch('singleton.datetime')
# # #     def test_batterycheck(self, mock_datetime, battery):
# # #         mock_datetime.now.return_value = datetime(2023, 5, 14, 12, 0, 0)
# # #         battery.data = {
# # #             'timing': {'beginning': 0},
# # #             'battery': {'level': 100, 'COST_PER_LV': 1}
# # #         }
# # #         assert battery.batterycheck() == 100
# # #
# # #         # 一分钟后，电量应该降低1
# # #         mock_datetime.now.return_value = datetime(2023, 5, 14, 12, 1, 0)
# # #         assert battery.batterycheck() == 99
# # #
# # #         # 一小时后，电量应该降低60
# # #         mock_datetime.now.return_value = datetime(2023, 5, 14, 13, 0, 0)
# # #         assert battery.batterycheck() == 40
# # #
# # #     @patch('singleton.datetime')
# # #     def test_reset(self, mock_datetime, battery):
# # #         mock_datetime.now.return_value = datetime(2023, 5, 14, 12, 0, 0)
# # #         battery.data = {
# # #             'timing': {'beginning': 0},
# # #             'battery': {'level': 50, 'COST_PER_LV': 1}
# # #         }
# # #         battery.reset()
# # #         assert battery.data['timing']['beginning'] != 0
# # #         assert battery.data['battery']['level'] == 100
# # #
# # #     @patch('singleton.datetime')
# # #     def test_save(self, mock_datetime, battery):
# # #         mock_datetime.now.return_value = datetime(2023, 5, 14, 12, 0, 0)
# # #         battery.data = {
# # #             'timing': {'beginning': 0},
# # #             'battery': {'level': 50, 'COST_PER_LV': 1}
# # #         }
# # #         with patch.object(json, 'dump', MagicMock()):
# # #             battery.save()
# # #             json.dump.assert_called_once_with(
# # #                 {'timing': {'beginning': 0}, 'battery': {'level': 49, 'COST_PER_LV': 1}},
# # #                 json.dump.call_args[0][0]
# # #             )
# # #
# # #     @patch('singleton.json')
# # #     def test_init(self, mock_json, battery):
# # #         mock_json.load.return_value = {
# # #             'timing': {'beginning': 0},
# # #             'battery': {'level': 50, 'COST_PER_LV': 1}
# # #         }
# # #         with patch('singleton.datetime') as mock_datetime:
# # #             mock_datetime.now.return_value = datetime(2023, 5, 14, 12, 0, 0)
# # #             battery.__init__()
# # #             assert battery.data == {
# # #                 'timing': {'beginning': datetime(2023, 5, 14, 12, 0, 0).timestamp()},
# # #                 'battery': {'level': 50, 'COST_PER_LV': 1}
# # #             }
# # #
# # #
# # # def test_singleton():
# # #     @singleton
# # #     class TestClass:
# # #         pass
# # #
# # #     assert isinstance(TestClass(), TestClass)
# # #     assert TestClass() is TestClass()