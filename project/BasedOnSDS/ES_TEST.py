import asyncio
from bleak import BleakClient
import datetime
import json
import traceback
import threadingz
import os
import Plugin

TEST_IMU_READ_UUID = [
    "00002a00-0000-1000-8000-00805f9b34fb", # bytearray(b'WT901-R3')
    "00002a01-0000-1000-8000-00805f9b34fb", # bytearray(b'\x00\x00')
    "00002a04-0000-1000-8000-00805f9b34fb", # bytearray(b'\x08\x00\x10\x00\x03\x00\x90\x01')
    "0000ffe4-0000-1000-8000-00805f9a34fb", # bytearray(b'\t')
    "0000ffe9-0000-1000-8000-00805f9a34fb", # bytearray(b'j')
]

TEST_IMU_NOTIFY_UUID = [
    "00002a1c-0000-1000-8000-00805f9b34fb", # bytearray(b'\x04d\x00\x00\xfe\x04')
    # "0000ffe4-0000-1000-8000-00805f9a34fb", # 多 bytearray(b"Ua\'\x00\xd8\xff\x00\x08\xe7\xff\xe9\xff\x01\x00\xab\xfd\x1c\xfe\xe58")
]

TEST_WRITE_UUID = [
    "00002a19-0000-1000-8000-00805f9b34fb",
    "00002a29-0000-1000-8000-00805f9b34fb",
    "00002a50-0000-1000-8000-00805f9b34fb",
]

CALIBRATE_SPAN    = 10 # seconds
COLLECT_TIME_SPAN = 0.2
DEBUG_SHOW        = True
ES_HOST_IP        = "127.0.0.1"
ES_HOST_PORT      = 40096
ERROR_MESSAGE     = {"type":"TypeError"}
FILEPATH          = os.path.dirname(__file__)
INVALID_DATA      = {
    "X"   : 0, "Y"   : 0, "Z"   : 0,
    "accX": 0, "accY": 0, "accZ": 0,
    "asX" : 0, "asY" : 0, "asZ" : 0
}
SENSOR_COUNT      = 6 # TODO
TIME_OUT_SPAN     = 1 # seconds
BATTERY_ORDER     = [0xFF, 0xAA, 0x27, 0x64, 0x00]
IMU_READ_UUID     = "0000FFE4-0000-1000-8000-00805F9A34FB"
IMU_SERVICE_UUID  = "0000FFE5-0000-1000-8000-00805F9A34FB",
IMU_WRITE_UUID    = "0000FFE9-0000-1000-8000-00805F9A34FB",

class DataTransform:
    def transform(self, data): # TODO: algorithm
        return Plugin.f(data)


class SensorCollector:
    def __init__(self, macAddr: str, name: str):
        self.macAddr       = macAddr
        self.name          = name
        self.cache         = None
        self.cacheTime     = datetime.datetime.utcnow()
        self.needCalibrate = False
        self.lastCalibrate = datetime.datetime.utcnow()
        self.connected     = False
        self.battery       = 0

    def __callback(self, sender, data):
        try:
            self.cache     = DataTransform().transform(data)
            self.cacheTime = datetime.datetime.utcnow()
            # print(data)
        except:
            pass

    def __connectionCheck(self) -> bool:
        timeNow = datetime.datetime.utcnow()
        delta   = timeNow - self.cacheTime
        if delta.total_seconds() > TIME_OUT_SPAN:
            return False
        else:
            return True
        
    def __batteryCheck(self, client: BleakClient) -> int: # TODO: read battery
        # print(self.cache)
        return 100
    
    def __calibrate(self, client) -> None: # TODO: calibrate
        self.needCalibrate = False

    async def __start_raw(self) -> None:
        while True:
            if DEBUG_SHOW:
                # print("[.] try to connect %s [%s]" % (self.macAddr, self.name), flush=True)
                pass
            try:
                client = BleakClient(self.macAddr)
                await client.connect()
            except:
                continue # just retry
            if DEBUG_SHOW:
                print("[+] connected with %s [%s]" % (self.macAddr, self.name), flush=True)

            for sid in client.services.services:
                for cid in client.services.services[sid].characteristics:
                    print(cid)

            def fn(sender, data):
                print("[=]", sender, data)

            await client.write_gatt_char(IMU_READ_UUID, bytearray(BATTERY_ORDER))
            dataRecv = await client.start_notify(IMU_READ_UUID, fn)
            print(dataRecv)
            await asyncio.sleep(1000)

            await client.start_notify(IMU_READ_UUID, lambda sender, data: self.__callback(sender, data))
            await asyncio.sleep(COLLECT_TIME_SPAN)
            while True:
                await asyncio.sleep(COLLECT_TIME_SPAN)
                self.connected = self.__connectionCheck()
                if not self.connected:
                    if DEBUG_SHOW:
                        print("[-] connection break with %s [%s]" % (self.macAddr, self.name), flush=True)
                        await client.disconnect()
                        break
                self.battery = self.__batteryCheck(client)
                if self.needCalibrate:
                    self.__calibrate(client) # TODO: calibrate
    def start(self):
        self.thread = threading.Thread(target=lambda: asyncio.run(self.__start_raw()))
        self.thread.start()

    def getRealtimeData(self):
        if not self.connected:
            return INVALID_DATA
        else:
            if self.cache is not None:
                return self.cache
            else:
                return INVALID_DATA

    def calibrate(self) -> bool:
        timeNow   = datetime.datetime.utcnow()
        deltaTime = timeNow - self.lastCalibrate
        if deltaTime.total_seconds() > CALIBRATE_SPAN:
            self.lastCalibrate = timeNow
            self.needCalibrate = True
            return True
        else:
            return False # fail to calibrate

    def getSensorStatus(self) -> dict:
        return {
            "connect": self.connected,
            "battery": self.battery
        }


class Transaction:
    def __init__(self, sensorCollectorList: list):
        assert type(sensorCollectorList) == list
        for sensorCollector in sensorCollectorList:
            assert isinstance(sensorCollector, SensorCollector)
        self.sensorCollectorList = sensorCollectorList

    def checkSuitable(self, dataInput: dict) -> bool:
        return False

    def getResponse(self, dataInput: dict) -> dict:
        return ERROR_MESSAGE


class Configuration:
    def __init__(self):
        filename = os.path.join(FILEPATH, "config.json")
        with open(filename, "r", encoding="utf-8") as fp:
            self.data = json.load(fp)
        assert type(self.data) == list and len(self.data) >= SENSOR_COUNT
        for item in self.data:
            assert type(item) == dict
            assert item.get("name") is not None
            assert item.get("macAddr") is not None

    def getJsonObject(self) -> list:
        return self.data
    
    def getMacAddrOfSensor(self, index):
        assert 0 <= index and index < SENSOR_COUNT # six sensor
        return self.data[index].get("macAddr")
    
    def getNameOfSensor(self, index):
        assert 0 <= index and index < SENSOR_COUNT # six sensor
        return self.data[index].get("name")

class RealTimeData(Transaction):
    def __init__(self, sensorCollectorList: list):
        super().__init__(sensorCollectorList)

    def checkSuitable(self, dataInput: dict) -> bool:
        return dataInput["type"] == "GetRealtimeData"
    
    def getResponse(self, dataInput: dict) -> list:
        ans = {}
        for sensorId, sensorCollector in enumerate(self.sensorCollectorList):
            sensorName = sensorCollector.name
            ans[sensorName] = sensorCollector.getRealtimeData()
        timeBase = datetime.datetime(1970, 1, 1, 0, 0, 0)
        delta    = datetime.datetime.utcnow() - timeBase
        ans["timestamp"] = delta.total_seconds()
        return ans


class SensorDetails(Transaction):
    def __init__(self, sensorCollectorList: list, config: Configuration):
        super().__init__(sensorCollectorList)
        self.config = config

    def checkSuitable(self, dataInput: dict) -> bool:
        return dataInput["type"] == "GetSensorDetails"
    
    def getResponse(self, dataInput: dict) -> dict:
        return self.config.getJsonObject()


class SensorStatus(Transaction):
    def __init__(self, sensorCollectorList: list):
        super().__init__(sensorCollectorList)

    def checkSuitable(self, dataInput: dict) -> bool:
        return dataInput["type"] == "GetSensorStatus"
    
    def getResponse(self, dataInput: dict) -> dict:
        ans = {}
        for index, sensorCollector in enumerate(self.sensorCollectorList):
            ans[str(index)] = sensorCollector.getSensorStatus()
        return ans


class SensorCalibration(Transaction):
    def __init__(self, sensorCollectorList: list):
        super().__init__(sensorCollectorList)

    def checkSuitable(self, dataInput: dict) -> bool:
        return dataInput["type"] == "SensorCalibration"
    
    def getResponse(self, dataInput: dict) -> dict:
        ans = True
        for sensorCollector in self.sensorCollectorList:
            tmpStatus = sensorCollector.calibrate()
            ans = ans and tmpStatus
        if ans:
            return {
                "type": "CalibrationSuccess"
            }
        else:
            return {
                "type": "CalibrationFailure"
            }


from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, routerObj) -> None:
        self.router = routerObj
        super().__init__(request, client_address, server)

    def do_POST(self):
        try:
            contentLength = int(self.headers['Content-Length'])
            dataInput     = self.rfile.read(contentLength).decode("utf-8")
            if DEBUG_SHOW: print("do_POST: %s" % dataInput)
            dataInput     = json.loads(dataInput)
            response      = self.router.getResponse(dataInput) # TODO: do not use singleton
        except:
            traceback.print_exc() # output error message
            response = ERROR_MESSAGE
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

class Router:
    def __init__(self):
        self.config = Configuration()
        self.sensorCollectorList = []
        for i in range(SENSOR_COUNT):
            macAddr = self.config.getMacAddrOfSensor(i)
            name    = self.config.getNameOfSensor   (i)
            self.sensorCollectorList.append(SensorCollector(macAddr, name))
        self.transactionList = [
            RealTimeData     (self.sensorCollectorList             ), 
            SensorDetails    (self.sensorCollectorList, self.config), 
            SensorStatus     (self.sensorCollectorList             ), 
            SensorCalibration(self.sensorCollectorList             )
        ]
    
    def getResponse(self, dataInput):
        for transcation in self.transactionList:
            if transcation.checkSuitable(dataInput):
                return transcation.getResponse(dataInput)
        return ERROR_MESSAGE

    def start(self, ip: str, port: int) -> None:
        # start sensor client
        for sensorCollector in self.sensorCollectorList:
            sensorCollector.start()
        # start http server
        this = self
        def __MyConstractor(request, client_address, server):
            obj = MyHttpRequestHandler(request, client_address, server, this)
            return obj
        server = HTTPServer((ip, port), __MyConstractor)
        print("Server started on http://%s:%d" % (ip, port))
        # print(self.transactionList)
        server.serve_forever()

import bleak
bleak.cli()

app = Router()
app.start(ES_HOST_IP, ES_HOST_PORT)
