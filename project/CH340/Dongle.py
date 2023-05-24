 #!/usr/bin/python
import serial
import threading
import datetime
import sys
import json
import socket
import time

BAUD_RATE       = 230400

UDP_AIM_IP      = "127.0.0.1" #
UDP_AIM_PORT    = 17328       # UDP AIM PORT
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def match_pre(text, temp):
    if len(text) < len(temp): return False
    return text[:len(temp)] == temp

# turn bytes into int list
def getListFromBytes(b: bytes):
    arr = []
    for x in b:
        arr.append(int(x))
    return arr

NORMAL_DATA_LEN = 20

# send the data to es
def send_data_out_to_es(name: str, data: bytes, timeNow: str):

    # discard invalid data
    if len(data) != NORMAL_DATA_LEN:
        print("warning: data length is not NORMAL_DATA_LEN = %d" % NORMAL_DATA_LEN)
        return

    # get data
    dataToSend = {
        "sensor-name": name,
        "data": getListFromBytes(data),
        "time":timeNow
    }
    bytesToSend = json.dumps(dataToSend)

    # send UDP request
    serverAddressPort = (UDP_AIM_IP, UDP_AIM_PORT)
    UDPClientSocket.sendto(bytesToSend.encode(), serverAddressPort)

# auto listen conn and save the data into conn
def autoListener(conn, line_cache: list, list_cache: dict, data_cache: dict):
    line = b""
    while True:
        line += conn.read()
        if line.find(b"\r\n") != -1:
            if line[-2:] == b"\r\n":
                now, line = line, b""
            else:
                now, line = line.split(b"\r\n", 1)

            # route to data_cache
            if match_pre(now, b"WIT-REV"):
                name    = (now.split(b'"', 2)[1]).decode("ascii")
                data    = now.split(b"0x", 1)[1][16:-2]
                timeNow = str(datetime.datetime.now())
                data_cache[name] = (data, timeNow)
                send_data_out_to_es(name, data, timeNow)
                # print(data_cache)

            elif match_pre(now, b"WIT-LIST-#"):
                num  = now.split(b":", 1)[0][11:]
                name = now.split(b'"', 2)[1]
                mac  = now.split(b" 0x")[1].split(b" ", 1)[0]
                list_cache[name.decode('ascii')] = (num.decode("ascii"), mac.decode("ascii"))

            else:
                line_cache.append(now)
                print(now)


class Dongle:
    def __init__(self, port:str, name_list:list):
        # initialization
        self.line_cache = []
        self.list_cache = {}
        self.data_cache = {} # from ID to newest data (20 bytes)

        # store local data
        self.port      = port
        self.name_list = name_list
        self.conn      = serial.Serial(port, BAUD_RATE)

        # create lisener thread
        self.th = threading.Thread(target=autoListener, args=(self.conn,
                                                                self.line_cache,
                                                                self.list_cache,
                                                                self.data_cache))
        self.th.start()

        # try to connect
        if not self.connected():
            raise AssertionError("Not Connected")

        # try to list devices
        if not self.list_devices():
            raise AssertionError("Sensors Not Found")

        # link discovered devices
        self.link_device()

    def link_device(self):
        for name in self.name_list:
            num, mac = self.list_cache[name]
            print("Connecting name = %s, num = %s" % (name, num))
            self.send("AT+CONNECT=" + num.strip())
            time.sleep(1)
        return True

    def send(self, ins: bytes):
        if type(ins) == str:
            ins = ins.encode("ascii")
        if ins[-2:] != b"\r\n": ins += b"\r\n"
        self.conn.write(ins)

    def list_devices(self):
        self.send("AT+SCAN=1")
        print("Scan_start")
        while True:
            if self.check_name_list():
                self.send("AT+SCAN=0")
                print("Sensors Got")
                return True


    def check_name_list(self):
        for name in self.name_list:
            print("Check Name %s" % name)
            if self.list_cache.get(name) is None:
                return False
        return True

    def has_line_cache(self):
        return len(self.line_cache) >= 1

    def pop_cache(self):
        self.line_cache = []

    def connected(self):
        self.send("AT")
        while not self.has_line_cache():
            pass
        if b"OK\r\n" in self.line_cache:
            self.pop_cache()
            return True
        return False

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        raise AssertionError("sys.argv len != 2")
    ttyUSB_name, device_name_list = json.loads(argv[1])
    print("[DEBUG]", ttyUSB_name, device_name_list)
    dongle = Dongle(ttyUSB_name, device_name_list)
