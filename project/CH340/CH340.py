import serial
import threading

DEV_PORT  = "COM6" # for linux: /dev/ttyUSB0 or /dev/ttyUSB1
BAUD_RATE = 230400

conn = serial.Serial(port=DEV_PORT, baudrate=BAUD_RATE)

def read_conn(conn):
    line = b""
    while True:
        ret = conn.read(1)
        line += ret
        if line.find(b"\r\n") != -1:
            if line[-2:] == "\r\n":
                part1, line = line, b""
            else:
                part1, line = line.split(b"\r\n", 1)
            print(part1 + b"\r\n")

th = threading.Thread(target=read_conn, args=(conn,))
th.start()

while True:
    ins = input(">>> ")
    ins = (ins + "\r\n").encode("ascii")
    conn.write(ins)