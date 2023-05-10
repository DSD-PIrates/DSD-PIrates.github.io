from ES import Router
from ES import MyHttpRequestHandler
import pytest
import datetime
import ES


import pytest


# (33) Test MyHttpRequestHandler.__init__(self, request, client_address, server, routerObj)
# def test_MyHttpRequestHandlerInit()



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