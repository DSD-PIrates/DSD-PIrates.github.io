import socket
import json

UDP_SERVER_IP   = "127.0.0.1"
UDP_SERVER_PORT = 17328
bufferSize      = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((UDP_SERVER_IP, UDP_SERVER_PORT))

def com_server_function():
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        dataNow = json.loads(message.decode())

        # output valid data
        if (    dataNow.get("sensor-name") is not None
            and dataNow.get("data"       ) is not None
            and dataNow.get("time"       ) is not None
        ):
            print(dataNow)

if __name__ == "__main__":
    com_server_function()
