import serial
import threading

BAUD_RATE = 230400
TIMEOUT = 10

conn = serial.Serial('/dev/ttyUSB0', BAUD_RATE)

def read_conn(conn):
    line = b""
    while True:
        ret = conn.read()
        line += ret
        if line[-2:] == b"\r\n":
            print(line)
            line = b""

th = threading.Thread(target=read_conn, args=(conn, ))
th.start()

while True:
    ins = (input(">>> ") + "\r\n").encode('ascii')
    conn.write(ins)
