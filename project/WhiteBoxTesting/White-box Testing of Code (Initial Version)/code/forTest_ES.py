import asyncio
import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
from bleak import BleakClient
import ES



CALIBRATE_SPAN    = 10 # seconds
COLLECT_TIME_SPAN = 0.2
DEBUG_SHOW        = True
ES_HOST_IP        = "127.0.0.1"
ES_HOST_PORT      = 40096
IMU_READ_UUID     = "0000FFE4-0000-1000-8000-00805F9A34FB"
ERROR_MESSAGE     = {"type":"TypeError"}
INVALID_DATA      = {
    "X"   : 0, "Y"   : 0, "Z"   : 0,
    "accX": 0, "accY": 0, "accZ": 0,
    "asX" : 0, "asY" : 0, "asZ" : 0
}
SENSOR_COUNT      = 6 # TODO
TIME_OUT_SPAN     = 1 # seconds
BATTERY_ORDER     = [0xFF, 0xAA, 0x27, 0x64, 0x00]



class TmpSensorCollector:
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
            self.cache     = ES.DataTransform().transform(data)
            self.cacheTime = datetime.datetime.utcnow()
            print(data)
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


    # 为了方便测试，代码有些修改
    async def __start_raw(self, client) -> None:
        # while True:
        if DEBUG_SHOW:
            # print("[.] try to connect %s [%s]" % (self.macAddr, self.name), flush=True)
            pass
        # client = BleakClient(self.macAddr)
        await client.connect()
        # try:
        #     client = BleakClient(self.macAddr)
        #     await client.connect()
        # except:
        #     pass
        #     # continue # just retry
        if DEBUG_SHOW:
            print("[+] connected with %s [%s]" % (self.macAddr, self.name), flush=True)
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
            await client.write_gatt_char(IMU_READ_UUID, bytearray(BATTERY_ORDER))
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
