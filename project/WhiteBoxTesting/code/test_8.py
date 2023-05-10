from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import threading
import requests
from unittest.mock import MagicMock, Mock
from ES import MyHttpRequestHandler
import socket
import pytest
import ES
import io
import json

from ES import MyHttpRequestHandler, Configuration, SENSOR_COUNT, SensorCollector, RealTimeData, SensorDetails, \
    SensorStatus, SensorCalibration, ERROR_MESSAGE
import forTest_ES
import requests
import datetime



# (35) Test MyHttpRequestHandler.do_POST(self)
class Router:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.config = Configuration()
        self.sensorCollectorList = []
        for i in range(SENSOR_COUNT):
            macAddr = self.config.getMacAddrOfSensor(i)
            name = self.config.getNameOfSensor(i)
            self.sensorCollectorList.append(SensorCollector(macAddr, name))
        self.transactionList = [
            RealTimeData(self.sensorCollectorList),
            SensorDetails(self.sensorCollectorList, self.config),
            SensorStatus(self.sensorCollectorList),
            SensorCalibration(self.sensorCollectorList)
        ]

    def getResponse(self, dataInput):
        for transcation in self.transactionList:
            if transcation.checkSuitable(dataInput):
                return transcation.getResponse(dataInput)
        return ERROR_MESSAGE

    def start(self, ip: str, port: int) -> None:
        # start sensor client
        # for sensorCollector in self.sensorCollectorList:
        #     sensorCollector.start()
        # # start http server
        # this = self

        def __MyConstractor(request, client_address, server):
            obj = MyHttpRequestHandler(request, client_address, server, Router())
            return obj

        self.server = HTTPServer((ip, port), __MyConstractor)

        # server = HTTPServer((ip, port), __MyConstractor)
        print("Server started on http://%s:%d" % (ip, port))
        # print(self.transactionList)


        # self.server.serve_forever()
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

@pytest.fixture(scope="module")
def server():
    router = Router()
    router.start("localhost", 40096)
    yield
    router.server.shutdown()
    router.server_thread.join()

    # def MyConstractor(request, client_address, server):
    #     obj = MyHttpRequestHandler(request, client_address, server, router)
    #     return obj
    # server = HTTPServer(('localhost', 40096), MyConstractor)
    # server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.start()
    # yield server
    # server.shutdown()
    # server_thread.join()

@pytest.mark.parametrize('dataInput, expected_val', [
    ({"type": "Test"}, {"type":"TypeError"}),
    ({"type": "GetSensorStatus"}, {"0": {"connect": False, "battery": 0}, "1": {"connect": False, "battery": 0}, "2": {"connect": False, "battery": 0}, "3": {"connect": False, "battery": 0}, "4": {"connect": False, "battery": 0}, "5": {"connect": False, "battery": 0}}),
    ({"type": "GetSensorDetails"}, [
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
                                    ]),
    ({"type": "SensorCalibration"}, {"type": "CalibrationFailure"})
])

def test_do_POST(server, dataInput, expected_val):
    conn = http.client.HTTPConnection("localhost", 40096)
    headers = {"Content-type": "application/json"}
    data = dataInput
    json_data = json.dumps(data)
    conn.request("POST", "/", json_data, headers)
    response = conn.getresponse()
    # assert text[0] == {"name": "R1", "macAddr": "F2:02:E0:8D:B8:05"}
    # assert text[1] == {"name": "R2", "macAddr": "C4:39:0D:A9:91:89"}
    # assert text[2] == {"name": "R3", "macAddr": "E8:67:FE:A6:D4:3C"}
    # assert text[3] == {"name": "L1", "macAddr": "D1:7A:2A:54:02:95"}
    # assert text[4] == {"name": "L2", "macAddr": "D7:0F:4F:1D:4F:B5"}
    # assert text[5] == {"name": "L3", "macAddr": "E6:7A:B7:B0:45:9D"}

    assert response.status == 200
    assert response.getheader("Content-type") == "text/json"
    response_data = response.read().decode("utf-8")
    assert response_data == json.dumps(expected_val)
