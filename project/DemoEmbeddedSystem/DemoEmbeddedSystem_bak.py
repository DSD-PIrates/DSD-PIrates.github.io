# This is a demo for CentralServer

import socket
import threading
import json
import importlib
import traceback

HOST = '139.155.89.85'
PORT = 11451
MBUF = 1048576 * 10 # Max buffer size 10MB

import DemoServerProcessor

def solve(bodydata: str):
    # try to get json data
    try:    jsonData = json.loads(bodydata)
    except: jsonData = None
    # if can not get json data
    if jsonData is None:
        return {
            "type": "Error",
            "message": "PostDataIsNotJson"
        }
    # form ans
    if type(jsonData) == dict and jsonData.get("type") == "Reload":
        try:
            importlib.reload(DemoServerProcessor)
            ans = {
                "type": "ReloadResponse",
                "message": "ReloadSucceed"
            }
        except:
            ans = None
            errorDetail = str(traceback.format_exc())
    else:
        try:
            ans = DemoServerProcessor.solve(jsonData)
            errorDetail = "ServerProcessFuctionForgetToReturn"
        except: 
            ans = None
            errorDetail = str(traceback.format_exc())
    # return ans to the client
    if ans is not None: return ans
    else: return {
        "type": "Error",
        "message": "ServerInnerError",
        "details": errorDetail
    }

# calculate the return value
def work(conn, addr):
    data = conn.recv(MBUF).decode()
    # print(f"[.] debug get data = {data}")
    # get body data
    try:    bodydata = data.split("\r\n\r\n", 1)[1]
    except: bodydata = None
    print(f"[.] debug get addr = {addr} data = {bodydata}")
    # get response for the request
    if bodydata is not None:
        ans = solve(bodydata)
    else:
        ans = {
            "type": "Error",
            "message": "NoPostData"
        }
    # parse data
    dataToSend  = json.dumps(ans).encode()
    httpHeader  = "HTTP/1.1 200 OK\r\n"
    httpHeader += "Content-Type: application/json\r\n"
    httpHeader += "Content-Length: " + str(len(dataToSend))
    mergedData  = (httpHeader + "\r\n\r\n").encode() + dataToSend
    conn.sendall(mergedData)
    conn.close()
    print(f"[-] closing {addr}")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"[.] listening {HOST}:{PORT}")
    while True:
        conn, addr = sock.accept()
        print(f"[+] connected by {addr}")
        t = threading.Thread(target=work, args=(conn, addr))
        t.start()
