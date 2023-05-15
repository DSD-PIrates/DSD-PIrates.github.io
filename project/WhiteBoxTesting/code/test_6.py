from ES import Router
from ES import MyHttpRequestHandler
import pytest
import datetime
import ES
import threading
from unittest.mock import AsyncMock, MagicMock
from unittest.mock import patch
import unittest
import socket
import http.client
import json
from http.server import HTTPServer



# (33) Test MyHttpRequestHandler.__init__(self, request, client_address, server, routerObj)
@pytest.fixture(scope="module")
def server():
    router = Router()
    def __MyConstractor(request, client_address, server):
        obj = MyHttpRequestHandler(request, client_address, server, router)
        return obj
    server = HTTPServer(('localhost', 40096), __MyConstractor)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    yield server
    server.shutdown()
    server_thread.join()

@pytest.mark.parametrize('dataInput, expected_val', [
    ({"type": "Test"}, {"type":"TypeError"}),
    ({"type": "GetSensorStatus"}, {'0': {'connect': False, 'battery': 100.0},
    '1': {'connect': False, 'battery': 100.0},
    '2': {'connect': False, 'battery': 100.0},
    '3': {'connect': False, 'battery': 100.0},
    '4': {'connect': False, 'battery': 100.0},
    '5': {'connect': False, 'battery': 100.0}
}),
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

def test_MyHttpRequestHandlerInit(server, dataInput, expected_val):
    # 创建 HTTP 连接和请求头
    conn = http.client.HTTPConnection("localhost", 40096)
    headers = {"Content-type": "application/json"}
    data = dataInput
    json_data = json.dumps(data)
    conn.request("POST", "/", json_data, headers)
    response = conn.getresponse()
    assert response.status == 200
    assert response.getheader("Content-type") == "text/json"
    response_data = response.read().decode("utf-8")
    assert response_data == json.dumps(expected_val)





# (34) Test Router.getResponse(self, dataInput)
@pytest.mark.parametrize('dataInput, expected_val', [
    ({"type":"GetSensorDetails"}, [
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
    ({"type":"Test"}, {'type': 'TypeError'})
])
def test_getResponse(dataInput, expected_val):
    testClass = Router()
    assert testClass.getResponse(dataInput) == expected_val