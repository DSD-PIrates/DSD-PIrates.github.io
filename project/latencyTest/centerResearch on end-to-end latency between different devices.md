#### <center>Research on end-to-end latency between different devices</center>

<center>Three kinds of HTTP transmission sensor real-time monitoring data (Android to PC, PC to cloud, Android to cloud) round-trip time delay (RTT) test</center>

```
Author: Aidan
```

##### 1. Testing from Android to PC:

a. Create an application on the Android device to read sensor data and send it via an HTTP POST request to a server on the PC.

b. Run a server program on the PC that receives sensor data sent by Android using HTTP and responds to requests.

c. Set a timer on the Android device to record the timestamp of the HTTP request sent to the server and the timestamp of the server response received on the Android device.

```java
//MainActivity.java
...
try {
    sendTime = System.currentTimeMillis();       //the timestamp of the HTTP request sent to the server
    SendHttpPost("http://10.151.243.55:8000", pairList); 
    receiveTime = System.currentTimeMillis();    //the timestamp of the server response received
} catch (IOException e) {
    e.printStackTrace();
}
...
```

d. Calculate the round-trip delay (RTT) by subtracting the timestamp of sending the HTTP request from the timestamp of receiving the response, and 1500 recorded data are in **final1.txt**.

| index | value(ms) |
| -------- | -------- |
| mean        | 26.8827       |
| Standard Deviation        | 20.8187       |

##### 2. Testing from PC to cloud:

a. Run the program on the PC to receive sensor data detected by Android device and send it via an HTTP POST request to the cloud.

b. Set up a server application on the cloud to receive sensor data.

c. Set a timer on the PC to record the timestamp of the HTTP request sent to the cloud and the timestamp of the cloud response received on the PC

```python
# AdaptorServer.py
...
f = open("record.txt", "wb+", buffering=0)
...
def relaySendData(inputData):
    ...
    ...
    if shouldSend(deviceName):
        copy_inputData.pop("deviceName") # delete this attribute
        time1 = getTimeNow()  # the timestamp of the HTTP request sent to the cloud
        ans = GDSC.writeDataToServer(deviceName, copy_inputData)
        time2 = getTimeNow()  # the timestamp of the cloud response received on the PC
        diff = str(time2 - time1)
        if ans != {"result": "connection failed"}:
            f.write(diff.encode('utf-8')+b"\n")
...
...
```

d. Calculate the round-trip delay (RTT) by subtracting the timestamp of sending the HTTP request from the timestamp of receiving the response, and 1500 recorded data are in **final2.txt**.
| index | value(ms) |
| -------- | -------- |
| mean        | 118.0380 |
| Standard Deviation        | 11.3257 |

##### 3. Testing from Android to cloud:

a. Create an application on the Android device to read sensor data and send it via an HTTP POST request to the cloud.

b. Set up a server application on the cloud to receive sensor data.

c. Set a timer on the Android device to record the timestamp of the HTTP request sent to the cloud and the timestamp of the server response received on the Android device.

```java
//MainActivity.java
...
try {
    sendTime = System.currentTimeMillis();       //the timestamp of the HTTP request sent to the server
    SendHttpPost("http://10.151.243.55:8000", pairList); 
    receiveTime = System.currentTimeMillis();    //the timestamp of the server response received
} catch (IOException e) {
    e.printStackTrace();
}
...
```

d. Calculate the round-trip delay (RTT) by subtracting the timestamp of sending the HTTP request from the timestamp of receiving the response, and 1500 recorded data are in **final3.txt**.
| index | value(ms) |
| -------- | -------- |
| mean        | 145.6800 |
| Standard Deviation        | 45.1560 |