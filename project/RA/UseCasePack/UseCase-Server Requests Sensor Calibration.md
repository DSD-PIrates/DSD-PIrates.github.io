

## Case: Server Requests Sensor Calibration

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

### Brief Introduction

When the server requests sensor calibration, the process starts; After the server receives the calibration success response or calibration failure response sent by the embedded system, the process ends.

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.

- The network is available and the server is able to send messages to the embedded system.
- The embedded system is not in **real-time data transmission mode**.

### Basic Flow

1. The server sends a sensor calibration **REQUEST**;
2. After receiving the request, the embedded system sends a response to the server and performs calibration;
3. After the embedded system calibrates the sensor successfully, it sends a **RESPONSE** to the server.
3. The server receives the information.

### Exception Flows

- 2a: When **REQUEST** received, if the embedded system is in **real-time data transmission mode**,  the embedded system **RESPONSE** the error message to the server, use case ends.

- 2b: When **REQUEST** received, if the sensors have been calibrated in the recently ten seconds, the embedded system will refuse to calibrate and **RESPONSE** the error message to the server, use case ends.
- 4a: If server failed to receive the information, the server will check the reachability of the embedded system, and Requests Sensor Calibration again if the embedded system is accessible.

### Post Conditions

1. The server will receive the information of calibration from the embedded system after the Basic Flow.

### Supplemental Requirements

During calibration, it should be ensured that the sensor is placed on a horizontal stand. The calibration here refers to the acceleration calibration. Since the acceleration of the sensor is measured by the acceleration due to gravity, calibration should be performed before use.

### Visual Model

<img src="./Server Requests Sensor Calibration.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |
