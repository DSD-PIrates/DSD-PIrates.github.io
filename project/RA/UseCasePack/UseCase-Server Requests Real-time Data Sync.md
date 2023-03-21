

## Case: Server Requests Real-time Data (Sync)

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

### Brief Introduction

When the server requests the data, the process starts; When the server gets the data from the embedded system, the process ends.

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.

- The network is available and the server is able to send messages to the embedded system.

### Basic Flow

1. The server **REQUESTs** to obtain real-time data, with the sampling rate attached.
1. The embedded system get the real-time data from the sensors.
1. The embedded system make a **RESPONSE** to the server.
4. The server receives the information.

### Exception Flows

- 4a: If the server fails to receive the real-time data from the embedded system, the server **WILL NOT** retry to request again, the data it should have received will be regarded as the latest cached data or an INVALID data (if there are no value cached).

### Post Conditions

1. Data received should be cached by the server.
2. The embedded system quits **real-time data transmission mode** after the Basic Flow.

For Exception Flow 10a, The server detected the embedded system offline.

### Supplemental Requirements

3. Depending on the network environment, the latency of real-time data may vary. Generally, real-time data has a delay of around 200 milliseconds.
3. Real-time data includes the angles, angular velocities, and accelerations in the XYZ directions, as well as the timestamp of the data sampling determined by the embedded system at the time of sampling.

### Visual Model

<img src="Server Requests Real-time Data.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |

