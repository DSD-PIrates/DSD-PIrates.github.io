import unittest
import http.client
import json


SERVER_IP   = "139.155.89.85"
SERVER_PORT = 11451

def makeError(msg):
    return {"type"   : "Error", "message": str(msg)}


def clientRequest(data: dict, serverIP: str, serverPort: int):
    assert type(data)       == dict
    assert type(serverIP)   ==  str
    assert type(serverPort) ==  int
    conn = http.client.HTTPConnection("%s:%d" % (serverIP, serverPort))
    jsonData = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    try:
        conn.request("POST", "/", jsonData, headers)
        response = conn.getresponse()
        body = response.read().decode()
    except:
        body = None
    if body is None:
        return makeError("CanNotConnectToServer")
    
    try:
        body = json.loads(body)
    except:
        body = None
    
    if body is not None:
        return body
    else:
        return makeError("ServerResponseIsNotJson")

class TestClientRequest(unittest.TestCase):

   

    def test_realtime_data(self):
        dataNow = {"type": "GetRealtimeData"}
        response = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
        self.assertIsNotNone(response)
        self.assertNotIn("Error", response)
        self.assertEqual(response.get('type'), 'GetRealtimeDataResponse')

    def test_sensor_status(self):
        dataNow = {"type":"GetSensorStatus"}
        response = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
        self.assertIsNotNone(response)
        self.assertNotIn("Error", response)
        self.assertEqual(response.get('type'), 'GetSensorStatusResponse') 
    
    def test_sensor_calibration(self):
        dataNow = {"type":"SensorCalibration"}
        response = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
        self.assertIsNotNone(response)
        self.assertNotIn("Error", response)
        self.assertEqual(response.get('type'), 'CalibrationSuccess') 

    def test_sensor_details(self):
        dataNow = {"type":"GetSensorDetails"}
        response = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
        self.assertIsNotNone(response)
        self.assertNotIn("Error", response)
        self.assertEqual(response.get('type'), 'GetSensorDetailsResponse')

    def test_sensor_ping(self):
        dataNow = {"type":"Ping"}
        response = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
        self.assertIsNotNone(response)
        self.assertNotIn("Error", response)
        self.assertEqual(response.get('type'), 'PingResponse')  
        
        
if __name__ == '__main__':
    unittest.main()
