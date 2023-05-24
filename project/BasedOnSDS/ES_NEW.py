import asyncio
# from bleak import BleakClient
import datetime
import json
import traceback
import threading
import os
import Plugin
import ComServer

CALIBRATE_SPAN    = 10 # seconds
# COLLECT_TIME_SPAN = 0.2
COLLECT_TIME_SPAN = 0.5
DEBUG_SHOW        = True
ES_HOST_IP        = "0.0.0.0"
ES_HOST_PORT      = 40096
IMU_READ_UUID     = "0000FFE4-0000-1000-8000-00805F9A34FB"
ERROR_MESSAGE     = {"type":"TypeError"}
FILEPATH          = os.path.dirname(__file__)
INVALID_DATA      = {
    "X"   : 0, "Y"   : 0, "Z"   : 0,
    "accX": 0, "accY": 0, "accZ": 0,
    "asX" : 0, "asY" : 0, "asZ" : 0
}
SENSOR_COUNT      = 6
TIME_OUT_SPAN     = 1 # seconds
BATTERY_ORDER     = [0xFF, 0xAA, 0x27, 0x64, 0x00]
SERVER_QUIT       = False


class DataTransform:
    def transform(self, data):
        return Plugin.f(data)


def singleton(cls):
    _instance = {}
    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

GLOBAL_CACHE = {}

# save cache to global
def save_cache_callback(data: dict):
    GLOBAL_CACHE[data["sensor-name"]] = data

th_com_server = threading.Thread(target=ComServer.com_server_function, args=(save_cache_callback,))
th_com_server.start()

@singleton
class Battery:
    def __init__(self) :
        filename = os.path.join(FILEPATH, "monitor.json")
        with open(filename, "r", encoding="utf-8") as fp:
            self.data = json.load(fp)
        self.data['timing']['beginning'] = datetime.datetime.now().timestamp()
    def batterycheck(self):
        return self.data['battery']['level'] - (datetime.datetime.now().timestamp() - self.data['timing']['beginning']) // 60000 // self.data['battery']['COST_PER_LV']
    def reset(self):
        self.data['timing']['beginning'] = datetime.datetime.now().timestamp()
        self.data['battery']['level'] = 100
    def save(self):
        self.data['battery']['level'] = self.batterycheck()
        filename = os.path.join(FILEPATH, "monitor.json")
        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(self.data, fp)

def get_real_name(old_name):
    return "WT901-" + old_name.split("(")[-1][:2]

def getBytesFromList(lis: list):
    ans = b""
    for x in lis:
        ans += x.to_bytes(1, "little")
    return ans

class SensorCollector:
    def __init__(self, macAddr: str, name: str):
        self.macAddr       = macAddr
        self.name          = name
        self.cache         = None
        self.cacheTime     = datetime.datetime.utcnow()
        self.needCalibrate = False
        self.lastCalibrate = datetime.datetime.utcnow()
        self.connected     = False
        self.battery       = Battery()

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

    def __batteryCheck(self, client) -> int:
        return self.battery.batterycheck()

    def __calibrate(self, client) -> None:
        self.needCalibrate = False

    async def __start_raw(self) -> None:
        while True and not SERVER_QUIT:
            if DEBUG_SHOW:
                # print("[.] try to connect %s [%s]" % (self.macAddr, self.name), flush=True)
                pass

            """
            try:
                client = BleakClient(self.macAddr)
                await client.connect()
            except:
                continue # just retry
            if DEBUG_SHOW:
                print("[+] connected with %s [%s] at %s" % (self.macAddr, self.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), flush=True)
            await client.start_notify(IMU_READ_UUID, lambda sender, data: self.__callback(sender, data))
            await asyncio.sleep(COLLECT_TIME_SPAN)
            """

            self.connected = True
            while True and not SERVER_QUIT:
                await asyncio.sleep(COLLECT_TIME_SPAN)
                # self.connected = self.__connectionCheck()
                if not self.connected:
                    if DEBUG_SHOW:
                        # print("[-] connection break with %s [%s] at %s" % (self.macAddr, self.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), flush=True)
                        # await client.disconnect()
                        self.battery.save()
                        break

                # self.battery = self.__batteryCheck(client)
                if self.needCalibrate:
                    self.__calibrate(client)

    def start(self):
        # self.thread = threading.Thread(target=lambda: asyncio.run(self.__start_raw()))
        # self.thread.start()
        pass

    def getRealtimeData(self):
        global GLOBAL_CACHE
        """
        if not self.connected:
            return INVALID_DATA
        else:
            if self.cache is not None:
                return self.cache
            else:
                return INVALID_DATA
        """
        real_name = get_real_name(self.name)
        if GLOBAL_CACHE.get(real_name) is None:
            return INVALID_DATA
        else:
            dataNow = getBytesFromList(GLOBAL_CACHE[real_name]["data"])
            return Plugin.f(dataNow)

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
            "battery": self.battery.batterycheck()
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
                "type": " CalibrationFailure"
            }


from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, routerObj) -> None:
        self.router = routerObj
        super().__init__(request, client_address, server)

    def do_GET(self):
        return self.do_POST()

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
        global SERVER_QUIT
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
        try:
            server.serve_forever()
        except:
            SERVER_QUIT = True
            print("[*] Server Quit ...")

app = Router()
app.start(ES_HOST_IP, ES_HOST_PORT)
