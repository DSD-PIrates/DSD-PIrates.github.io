

## Case: Server Checks Whether the Embedded System is Reachable

| Author | Version | Statue    | Date       |
| ------ | ------- | --------- | ---------- |
| Aidan  | 1       | Unaudited | 2023-03-19 |

### Brief Introduction

When the server wants to check if the embedded system is reachable, it sends an HTTP request message to the embedded system, and the process begins. When the server receives a response message from the embedded system, the process ends.

### Actors

- Server

### Pre-Conditions

- The embedded system has been powered on.
- The network is smooth and the server is able to send messages to the embedded system.

### Basic Flow

1. The server sends an  **request** message to the embedded system to determine whether the embedded system is available.
2. The embedded system receives the request sent by the server.
3. The embedded system send the **response** message to the server.
4. The server receives the response message.

### Exception Flows

- 3a:
  1. The server sends an HTTP request message to the embedded system to determine if it is accessible.
  2. The embedded system receives the request message sent by the server.
  3. The embedded system send the response message to the server.
  4. The server does not receive the response message due to network error, the use case ends.

### Post Conditions

1. The server confirms that the embedded system is working properly and accessible.

In Exception Flow 3a, server will not get the response from the embedded system, the server need to decide whether to send the response again.

### Supplemental Requirements



### Visual Model

<img src="./Server Checks Whether the Sensor is Reachable.svg" style="zoom:150%;" />

### Revision History

| Version | Date       | Author | Description      | Status    |
| ------- | ---------- | ------ | ---------------- | --------- |
| 1       | 2023-03-19 | Aidan  | Original Version | Unaudited |
