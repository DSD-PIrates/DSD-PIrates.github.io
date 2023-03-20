

## Case: Server Requests Real-time Data

| Author | Version | Statue    | Date       |
| ------ | ------- | --------- | ---------- |
| Aidan  | 1       | Unaudited | 2023-03-19 |

### Brief Introduction

When the server requests the data that the sensor starts detecting, the process starts; When the server requests to stop transmitting data, the process ends.

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.
- The network is smooth and the server is able to send messages to the embedded system.

### Basic Flow

1. The server **requests** to obtain real-time data.
1. The embedded system gets the request and send the **response** that it is ready.
1. The embedded system gets real-time data and **send** it back to server (Data transition will be activated at most five times per second.).
1. the server get the real-time data and **response** to the embedded system that it has got the data correctly.
1. Repeat steps 3 and 4 for several times until the server no longer wants to continue receiving data.
4. The server **requests** to stop sending real-time data.
4. The embedded system stop the detection of real-time data.
4. The embedded system **response** to server that the transmission has been stopped.
4. The server receives the information.

### Exception Flows

- 2a：
  1. The server requests to obtain real-time data.
  2. The embedded system gets the request and response that it is ready.
  2. The embedded system begin to acquire real-time data
  3. The embedded system acquires real-time data from the sensors and transmits it to the server, but the transmission is lost and no confirmation is received from the server.
  4. Due to the high frequency of data detection, the lost data is discarded and the next piece of data will be transmitted.
  5. The server requests to stop transmitting data.
  5. The transmission connection with the server is disconnected, and the sensor stops detecting data.

### Post Conditions

1. Data received should be cached by server;
1. Then users can decide whether to upload or discard the monitored data;
2. The application returns to the state before data request.

### Supplemental Requirements



### Visual Model

<img src="Server Requests Real-time Data.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author | Description      | Status    |
| ------- | ---------- | ------ | ---------------- | --------- |
| 1       | 2023-03-19 | Aidan  | Original Version | Unaudited |

