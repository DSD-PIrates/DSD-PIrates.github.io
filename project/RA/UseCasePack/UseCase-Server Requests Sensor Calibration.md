

## Case: Server Requests Sensor Calibration

| Author | Version | Statue    | Date       |
| ------ | ------- | --------- | ---------- |
| Aidan  | 1       | Unaudited | 2023-03-19 |

### Brief Introduction

When the server requests sensor calibration, the process starts; After the server receives the calibration success response or calibration failure response sent by the embedded system, the process ends.

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.
- The network is smooth and the server is able to send messages to the embedded system.

### Basic Flow

1. The server sends a sensor calibration **request**;
2. After receiving the request, the embedded system sends a response to the server and performs calibration;
3. After the embedded system calibrates the sensor successfully, it sends a **response** to the server.
3. The server receives the information.

### Exception Flows

- 2a:
  1. The server sends a sensor calibration request;
  2. The request sent by the server is lost, the embedded system does not receive the request, and the Use Case Ends;
- 3a:
  1. The server sends a sensor calibration request;
  2. After receiving the request, the embedded system sends a response to the server for calibration;
  3. After the embedded system calibrates the sensor successfully, it sends a response to the server, but the response is lost, and the server does not receive the response;
  4. After the timeout, the server resends the sensor calibration request;
  5. After receiving the request, the embedded system sends a response to the server for calibration;
  6. After the embedded system calibrates the sensor successfully, it sends a response to the server.

### Post Conditions



### Supplemental Requirements



### Visual Model

<img src="./Server Requests Sensor Calibration.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author | Description      | Status    |
| ------- | ---------- | ------ | ---------------- | --------- |
| 1       | 2023-03-19 | Aidan  | Original Version | Unaudited |
