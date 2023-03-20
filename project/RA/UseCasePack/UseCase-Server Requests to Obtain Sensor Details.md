

## Case: Server Requests to Obtain Sensor Details

| Author | Version | Statue    | Date       |
| ------ | ------- | --------- | ---------- |
| Aidan  | 1       | Unaudited | 2023-03-19 |

### Brief Introduction

When the server requests to obtain the sensor details, the process begins; it ends when the server confirms the signal has been received.

### Actors

- Server
- User

### Pre-Conditions

- The embedded system has been powered on.
- The network is smooth and the server is able to send messages to the embedded system.

### Basic Flow

2. The server **requests** to obtain the sensor details, including sensor model, sensor serial number.
2. The embedded begin to connect with the sensors and acquire the sensor details.
2. The embedded system  **response** sensors' details to the server.
2. The server receives the information.

### Exception Flows

- 2a：
  1. The server requests to obtain the sensor details, including sensor model, sensor serial number.
  2. The use case ends as the sensor did not receive the request.
- 3a:
  1. The server requests to obtain the sensor details, including sensor model, sensor serial number.
  2. The sensor receives the request and sends its own details to the server.
  3. If the server does not receive the information, it will request to obtain the sensor details again after a timeout.
  4. The sensor receives the request and sends its own details to the server again.
  5. The server receives the information and returns a response.

### Post Conditions

1. Server can obtain sensor details, including sensor model, sensor serial number.
2. The application returns to the state before request.

### Supplemental Requirements



### Visual Model

<img src="./Server Requests Sensor Details.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author | Description      | Status    |
| ------- | ---------- | ------ | ---------------- | --------- |
| 1       | 2023-03-19 | Aidan  | Original Version | Unaudited |
