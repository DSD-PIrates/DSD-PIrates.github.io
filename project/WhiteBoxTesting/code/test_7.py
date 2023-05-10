from ES import MyHttpRequestHandler
import pytest
import ES
import io
import json
from unittest.mock import Mock
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
# from ES import MyHttpRequestHandler
# from ES import Router

import pytest
import json
import threading
import requests
from io import BytesIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import MagicMock
from ES import MyHttpRequestHandler, Router
import socket

# class TestMyHttpRequestHandler:

#     def test_do_POST(self, monkeypatch):
#         # Create a mock Router object
#         mock_router = MagicMock()

#         # Create a mock POST request
#         data = {'key': 'value'}
#         body = BytesIO(json.dumps(data).encode('utf-8'))
#         headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#         mock_request = MagicMock(spec=BaseHTTPRequestHandler)
#         mock_request.headers = headers
#         mock_request.rfile = BytesIO()
#         mock_request.rfile.write(body.getvalue())
#         mock_request.rfile.seek(0)

#         # Create a real socket object
#         real_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#         # Convert the real socket object to a mock object
#         mock_socket = MagicMock(spec=real_socket)

#         # Set the mock socket object as the attribute of the mock request object
#         mock_request.connection = mock_socket

#         # Create a mock HTTP server
#         mock_server = HTTPServer(('localhost', 0), MyHttpRequestHandler)

#         # Create a MyHttpRequestHandler object
#         test_obj = MyHttpRequestHandler(mock_request, '127.0.0.1', mock_server, mock_router)

#         # Replace the self.router attribute with the mock router object
#         monkeypatch.setattr(test_obj, 'router', mock_router)

#         # Start the HTTP server in a new thread
#         server_thread = threading.Thread(target=mock_server.serve_forever)
#         server_thread.start()

#         # Create a mock POST request to the test server
#         port = mock_server.server_address[1]
#         url = 'http://localhost:%d/' % port
#         headers = {'content-type': 'application/json'}
#         response = requests.post(url, headers=headers, json=data)

#         # Stop the HTTP server
#         mock_server.shutdown()
#         server_thread.join()

#         # Check that the mock router object was called with the expected argument
#         mock_router.getResponse.assert_called_once_with(data)

#         # Check that the response was sent with the expected status code and body
#         assert response.status_code == 200
#         assert response.json() == mock_router.getResponse.return_value

# class MockRouter:
#     def getResponse(self, dataInput):
#         return {"output": "mocked_output"}


# class MockRequestHandler(BaseHTTPRequestHandler):
#     def __init__(self, *args, **kwargs):
#         self.router = MockRouter()
#         # self.server = kwargs.pop('server')
#         super().__init__(*args, **kwargs)

#     def do_POST(self):
#         try:
#             contentLength = int(self.headers['Content-Length'])
#             dataInput     = self.rfile.read(contentLength).decode("utf-8")
#             if DEBUG_SHOW: print("do_POST: %s" % dataInput)
#             dataInput     = json.loads(dataInput)
#             response      = self.router.getResponse(dataInput) # TODO: do not use singleton
#         except:
#             traceback.print_exc() # output error message
#             response = ERROR_MESSAGE
#         self.send_response(200)
#         self.send_header('Content-type', 'text/json')
#         self.end_headers()
#         self.wfile.write(json.dumps(response).encode("utf-8"))




# # Send a JsonData HTTP-POST request to (serverIP, serverPort)
# def clientRequest(data: dict, serverIP: str, serverPort: int):
#     # assert type(data)       == dict
#     # assert type(serverIP)   ==  str
#     # assert type(serverPort) ==  int
#     conn = http.client.HTTPConnection("%s:%d" % (serverIP, serverPort))
#     jsonData = json.dumps(data)
#     # jsonData = data
#     headers = {
#         "Content-Type": "application/json"
#     }
#     try:
#         conn.request("POST", "/", jsonData, headers)
#         response = conn.getresponse()
#         body = response.read().decode()
#     except:
#         body = None
#     if body is None: return makeError("CanNotConnectToServer")
#     # try to make it json
#     try:    body = json.loads(body)
#     except: body = None
#     # return if it is json
#     if body is not None: return body
#     else:                return makeError("ServerResponseIsNotJson")

# # "dataNow" is the JSON data to send, "ret" is the response from EmbeddedSystem
# dataNow = {
#     "name": "Test"
# }
# # dataNow = [1,2]
# ret = clientRequest(dataNow, SERVER_IP, SERVER_PORT)
# print(ret)




# # (35) Test MyHttpRequestHandler.do_POST(self)
# def test_do_POST():
# # def test_student(self):
#     headers = {
#         "Content-Type": "application/json"
#     }#请求头，以json形式发送
#     dataNow = {
#         "name": "Test"
#     }
#     # data = {
#     #     "id": "2018011",
#     #     "name": "小小",
#     #     "course": "数学",
#     # }#请求的参数，类似于postman发送
#     url = 'http://XXX/XXX'#请求地址
#     r = requests.post(url=url, data=json.dumps(data), headers=headers)
#     assert r.status_code == 200
#     assert r.json()['XXX'] == 'XXX'#对得到的结果进行判断

