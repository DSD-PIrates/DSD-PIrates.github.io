

## Case: Server Requests to Obtain the Sensor Status

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

### Brief Introduction

When the server requests to obtain the sensor status, the process begins; it ends when the server confirms the response has been received.

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.
- The network is available and the server is able to send messages to the embedded system.

### Basic Flow

1. The server **REQUESTs** to obtain the current status of the sensor, including sensor connection status, sensor power.
2. The embedded system receives the request and try to connect with the sensors.
2. The sensors reply the embedded system with their status and power.
2. The embedded system collects the data from sensors and makes a **RESPONSE** to the server.
3. The server receives the information.

### Exception Flows

- 2a：
  1. The embedded system receives the request and sends the request to the sensors.
  2. If the embedded system did not receive the response, the embedded system resend the request to the sensor for at most three times.
  2. If some sensor fails to response for three times, it will be regarded as **OFF**, return to Basic Flow step 4.
- 5a:
  1. If the server can not receives the **RESPONSE** from the embedded system. The server resend the **REQUEST** as in Basic Flow step 1 for at most three times, if the server gets the **RESPONSE** from the embedded system, use case ends normally. There should be a 0.5-second interval between two **REQUESTs**.
  2. After three unsuccessful attempts, the server determines that the embedded system is unreachable, use case ends with exception.

### Post Conditions

1. Users can obtain sensor status information, including sensor power after the Basic Flow ends.

### Supplemental Requirements

None.

### Visual Model

<img src="Server Requests Sensor Status.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |

