

## Case: Server Requests to Obtain Sensor Details

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

### Brief Introduction

When the server requests to obtain the sensor details, the process begins, it ends when the server confirms the response has been received. 

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.

- The network is available and the server is able to send messages to the embedded system.

### Basic Flow

1. The server **REQUESTs** to obtain the sensor details, including sensor name, sensor type and sensor serial number.

2. The embedded system  **RESPONSE** sensors' details to the server.
2. The server receives the information.

### Exception Flows

- 5a：
  1. If the server does not receive the **RESPONSE**, it should check the reachability of the embedded system, and try to obtain the sensor details again if the embedded system is reachable (return to Basic Flow step 1).
  2. If the embedded system is not reachable, use case ends.

### Post Conditions

1. Server can obtain sensor details, including sensor model, sensor serial number.
2. The application returns to the state before request.

### Supplemental Requirements

1. The details of the sensors are part of the configuration data of the embedded system, even when some sensor runs out of battery, the sensor details **CAN** still be acquired.

2. Sensor details contain sensor name, sensor type and sensor serial number.

### Visual Model

<img src="./Server Requests Sensor Details.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |
