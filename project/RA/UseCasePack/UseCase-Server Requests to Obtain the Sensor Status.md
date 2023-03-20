

## Case: Server Requests to Obtain the Sensor Status

| Author   | Version | Statue    | Date       |
| -------- | ------- | --------- | ---------- |
| Somebody | 1       | Unaudited | 2023-03-19 |

### Brief Introduction

When the server requests to obtain the sensor status, the process begins; it ends when the server confirms the signal has been received.

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.
- The network is smooth and the server is able to send messages to the embedded system.

### Basic Flow

1. The server **requests** to obtain the current status of the sensor, including sensor connection status, sensor power.
2. The embedded system receives the request and try to connect with the sensors.
2. The sensors get the connection and reply with their status and power to the embedded system.
2. The embedded system collects the data from sensors and **response** it to the server.
3. The server receives the information.

### Exception Flows

- 2a：
  1. The server requests to obtain the current status of the sensor, including sensor connection status, sensor power.
  1. The embedded system receives the request and sends the request to the sensors.
  2. If the embedded system did not receive the response, the embedded system resend the request to the sensor for at most three times.
  2. If some sensor does not response, embedded system report the error message to the server.
- 4a:
  1. The server requests to obtain the current status of the sensor, including sensor connection status, sensor power.
  2. The embedded system receives the request and sends the request to the sensors.
  3. The sensors get the request and reply with their status and power to the embedded system.
  4. The embedded system collects the response from sensors and send it to the server.
  5. If the HTTP connection between server and the embedded system corrupts, the user case ends.

### Post Conditions

1. Users can obtain sensor status information, including sensor connection status, sensor power.
2. The application returns to the state before status request.

In Exception Flow 4a, the server will not get the information from the embedded system, the server need to decide whether to send the request again to acquire the response.

### Supplemental Requirements



### Visual Model

<img src="Server Requests Sensor Status.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author   | Description      | Status    |
| ------- | ---------- | -------- | ---------------- | --------- |
| 1       | 2023-03-19 | Somebody | Original Version | Unaudited |

