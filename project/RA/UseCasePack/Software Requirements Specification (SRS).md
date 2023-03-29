# Software Requirements Specification (SRS)

Revision History:

| Data      | Author     | Description                           |
| --------- | ---------- | ------------------------------------- |
| 2023-3-23 | Aidan, Bob | Draft                                 |
| 2023-3-24 | Aidan, Bob | Add Sequences                         |
| 2023-3-26 | Aidan, Bob | Modify the workflow to a tabular form |
| 2023-3-28 | Aidan, Bob | Improve the overall structure of SRS  |
| 2023-3-29 | Aidan, Bob | Delete one Use Case                   |
|           |            |                                       |
|           |            |                                       |

[TOC]

## 1. Introduction

### 1.1 Intended Audience and Purpose

This document is intended to provided information guiding the development process, ensuring that all system requirements are met. The following entities may find the document useful:

Primary Customer - This page will detail all of the application requirements as understood by the production team. The customer should be able to determine that their requirements will be correctly reflected in the final product through the information found on this page.

User - A prospective user will be able to use this document to identify the main functionailty included in the application. Furthermore, the application will have a set of system requirements before the application can be run. Details regarding these requirements can be found here.

Development Team - Details of specific requirements that the final software build must include will be located here. Developers can use this document to ensure the software addresses each of these requirements.

QA Team - By developing testing procedures founded in the system requirements, the QA Team can create a comprehensive testing regimen that will guarantee requirements are met.

### 1.2 How to use the document
Table of Contents:

1. Introduction

2. Concept of Operations - broad description of the purpose of the application
    2.1 System Context - details any specific system requirements the application will require to run
    2.2 System Capabilities - description in prose of all capabilities available to the user in the interation
    2.3 Use cases - A detailed look at each functional requirement, describing the application context both before and after an action is taken

3. Use Cases

4. Behavioral Requirements - How the application will interact with a user
    4.1 Input and output requirements - A description of allowed inputs and generated outputs
           4.1.1 Input - Describes any restrictions that will be placed on allowed input
           4.1.2 Output - Describes the range of outputs that can be generated
    4.2 Detailed Output Behavior - Output descriptions in prose

    4.3 Quality Requirements - Requirements not pertaining to the function of the application will be listed here

5. Expected Subsets - Expected levels of functionality at checkpoints during development

6. Fundamental Assumptions - Some specifics about input, output, or behavior upon which other requirements are founded will be listed here

7. Expected Changes - Future features and directions the project is expected to take

8. Appendices - Details aiding the understanding of this document
    8.1 Definitions and acronyms - Any technical terms or abbreviations will be spelled out here for ease of use of the document
           8.1.1 Definitions - Definitions of technical or unusual terminology
           8.1.2 Acronyms and Abbreviations - Any abbreviated terms will be expanded here
    8.2 References - any external references necessary or helpful to understanding this document will be listed here

## 2. Concept of Operations

### 2.1 System Context
**System Requirements:**

*暂时为空

### 2.2 System capabilities
*暂时为空

## 3. Use Cases

![](./UseCaseDiagram/combination.svg)

​		

### 3.1 Case 1: Server Requests Real-time Data

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

**Brief Introduction**

When the server requests the data, the process starts; When the server gets the data from the embedded system, the process ends.

**Actors**

- Server

**Pre-Conditions**

- The embedded system has been powered on.

- The network is available and the server is able to send messages to the embedded system.

**Basic Flow**

| **Basic Flow** | Actor                                                        | System                                                       |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1              | The server **REQUESTs** to obtain real-time data, with the sampling rate attached. |                                                              |
| 2              |                                                              | The embedded system get the real-time data from the sensors. |
| 3              |                                                              | The embedded system make a **RESPONSE** to the server.       |
| 4              | The server receives the information.                         |                                                              |

**Exception Flows**

| 4a   | Actor                                                        | System                 |
| ---- | ------------------------------------------------------------ | ---------------------- |
|      |                                                              | From Basic Flow step 3 |
| 1    | If the server fails to receive the real-time data from the embedded system, the server **WILL NOT** retry to request again, the data it should have received will be regarded as the latest cached data or an INVALID data (if there are no value cached). |                        |

**Post Conditions**

1. Data received should be cached by the server.

For Exception Flow 4a, The server detected the embedded system offline.

**Supplemental Requirements**

1. Depending on the network environment, the latency of real-time data may vary. Generally, real-time data has a delay of around 200 milliseconds.

2. Real-time data includes the angles, angular velocities, and accelerations in the XYZ directions, as well as the timestamp of the data sampling determined by the embedded system at the time of sampling.

**Visual Model**

<img src="./UseCaseDiagram/Server Requests Real-time Data.svg" style="zoom:150%;" />

**Sequence Diagram**

![](./SequenceDiagram/RequestRealtimeData.svg)

**Revision History**

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |

​		

​	

### 3.2 Case 2: Server Checks Whether the Embedded System is Reachable

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

**Brief Introduction**

When the server wants to check if the embedded system is reachable, it sends an HTTP request message to the embedded system, and the process begins. When the server receives a response message from the embedded system, the process ends.

**Actors**

- Server

**Pre-Conditions**

- The embedded system has been powered on.

**Basic Flow**

| **Basic Flow** | Actor                                                        | System                                                       |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1              | The server sends an  **REQUEST** message to the embedded system to determine whether the embedded system is available. |                                                              |
| 2              |                                                              | The embedded system receives the request sent by the server. |
| 3              |                                                              | The embedded system send the **RESPONSE** message to the server. |
| 4              | The server receives the response message.                    |                                                              |

**Exception Flows**

| 3a   | Actor | System                                                       |
| ---- | ----- | ------------------------------------------------------------ |
|      |       | From Basic Flow step 2                                       |
| 1    |       | When the embedded system send the response, a network error occurs. |
| 2    |       | The embedded system do nothing, use case ends.               |

| 4a   | Actor                                                        | System                 |
| ---- | ------------------------------------------------------------ | ---------------------- |
|      |                                                              | From Basic Flow step 3 |
| 1    | When the server receives the response message, a network error occurs. |                        |
| 2    | The server makes another attempt to send a **REQUEST**, server will retry for at most three times. There should be a 0.5-second interval between two **REQUESTs**. If server get the **RESPONSE** from the embedded system, return to Basic Flow step 4. |                        |
| 3    | After server has been failed to connect for three times, server confirms that the embedded system is unreachable, use case ends. |                        |

**Post Conditions**

1. The server confirms that the embedded system is working properly and accessible.

In Exception Flow 4a, server confirms that the embedded system is inaccessible.

**Supplemental Requirements**

1. The Reachability check will be used under many conditions. For example, when a user checks whether an embedded system is connected to the network, the server needs to have a clear understanding of the accessibility of the embedded system, so the server begins a reachability check.
2. During communication, we require that **REQUEST** and **RESPONSE** must correspond one-to-one. Otherwise, it indicates that a network failure has occurred and Exception Flows are triggered. (This constraint applies to all communication issues mentioned later.)

**Visual Model**

<img src="./UseCaseDiagram/Server Checks Whether the Sensor is Reachable.svg" style="zoom:150%;" />

**Sequence Diagram**

![](./SequenceDiagram/checkAccessibility.svg)

**Revision History**

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |

​			

​	

### 3.3 Case 3: Server Requests Sensor Calibration

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

**Brief Introduction**

When the server requests sensor calibration, the process starts; After the server receives the calibration success response or calibration failure response sent by the embedded system, the process ends.

**Actors**

- Server

**Pre-Conditions**

- The embedded system has been powered on.
- The network is available and the server is able to send messages to the embedded system.

**Basic Flow**

| **Basic Flow** | Actor                                              | System                                                       |
| -------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| 1              | The server sends a sensor calibration **REQUEST**; |                                                              |
| 2              |                                                    | After receiving the request, the embedded system sends a response to the server and performs calibration; |
| 3              |                                                    | After the embedded system calibrates the sensor successfully, it sends a **RESPONSE** to the server. |
| 4              | The server receives the information.               |                                                              |

**Exception Flows**

| 2a   | Actor                  | System                                                       |
| ---- | ---------------------- | ------------------------------------------------------------ |
|      | From Basic Flow step 1 |                                                              |
| 1    |                        | When **REQUEST** received, if the sensors have been calibrated in the recently ten seconds, the embedded system will refuse to calibrate and **RESPONSE** the error message to the server, use case ends. |

| 4a   | Actor                                                        | System                 |
| ---- | ------------------------------------------------------------ | ---------------------- |
|      |                                                              | From Basic Flow step 3 |
| 1    | If server failed to receive the information, the server will check the reachability of the embedded system, and Requests Sensor Calibration again if the embedded system is accessible. |                        |

**Post Conditions**

1. The server will receive the information of calibration from the embedded system after the Basic Flow.

**Supplemental Requirements**

During calibration, it should be ensured that the sensor is placed on a horizontal stand. The calibration here refers to the acceleration calibration. Since the acceleration of the sensor is measured by the acceleration due to gravity, calibration should be performed before use.

**Visual Model**

<img src="./UseCaseDiagram/Server Requests Sensor Calibration.svg" style="zoom:150%;" />

**Sequence Diagram**

![](./SequenceDiagram/RequestSensorCalibration.svg)

**Revision History**

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |

​			

​	

### 3.4 Case 4: Server Requests to Obtain Sensor Details

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

**Brief Introduction**

When the server requests to obtain the sensor details, the process begins, it ends when the server confirms the response has been received. 

**Actors**

- Server

**Pre-Conditions**

- The embedded system has been powered on.

- The network is available and the server is able to send messages to the embedded system.

**Basic Flow**

| **Basic Flow** | Actor                                                        | System                                                       |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1              | The server **REQUESTs** to obtain the sensor details, including sensor name, sensor type and sensor serial number. |                                                              |
| 2              |                                                              | The embedded system  **RESPONSE** sensors' details to the server. |
| 3              | The server receives the information.                         |                                                              |

**Exception Flows**

| 3a   | Actor                                                        | System                 |
| ---- | ------------------------------------------------------------ | ---------------------- |
|      |                                                              | From Basic Flow step 2 |
| 1    | If the server does not receive the **RESPONSE**, it should check the reachability of the embedded system, and try to obtain the sensor details again if the embedded system is reachable (return to Basic Flow step 1). |                        |
| 2    | If the embedded system is not reachable, use case ends.      |                        |

**Post Conditions**

1. Server can obtain sensor details, including sensor model, sensor serial number.
2. The application returns to the state before request.

**Supplemental Requirements**

1. The details of the sensors are part of the configuration data of the embedded system, even when some sensor runs out of battery, the sensor details **CAN** still be acquired.

2. Sensor details contain sensor name, sensor type and sensor serial number.

**Visual Model**

<img src="./UseCaseDiagram/Server Requests Sensor Details.svg" style="zoom:150%;" />

**Sequence Diagram**

![](./SequenceDiagram/RequestSensorDetails.svg)

**Revision History**

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |

​			

​	

### 3.5 Case 5: Server Requests to Obtain the Sensor Status

| Author     | Version | Statue    | Date       |
| ---------- | ------- | --------- | ---------- |
| Aidan, Bob | 1       | Unaudited | 2023-03-21 |

**Brief Introduction**

When the server requests to obtain the sensor status, the process begins; it ends when the server confirms the response has been received.

**Actors**

- Server

**Pre-Conditions**

- The embedded system has been powered on.
- The network is available and the server is able to send messages to the embedded system.

**Basic Flow**

| **Basic Flow** | Actor                                                        | System                                                       | Sensor                                                       |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1              | The server **REQUESTs** to obtain the current status of the sensor, including sensor connection status, sensor power. |                                                              |                                                              |
| 2              |                                                              | The embedded system receives the request and try to connect with the sensors. |                                                              |
| 3              |                                                              |                                                              | The sensors reply the embedded system with their status and power. |
| 4              |                                                              | The embedded system collects the data from sensors and makes a **RESPONSE** to the server. |                                                              |
| 5              | The server receives the information.                         |                                                              |                                                              |

**Exception Flows**

| 2a   | Actor                   | System                                                       | Sensor                                                       |
| ---- | ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
|      | From Basic Flow step 1. |                                                              |                                                              |
| 1    |                         | The embedded system receives the request and sends the request to the sensors. |                                                              |
| 2    |                         | If the embedded system did not receive the response, the embedded system resend the request to the sensor for at most three times. |                                                              |
| 3    |                         |                                                              | If some sensor fails to response for three times, it will be regarded as **OFF**, return to Basic Flow step 4. |

| 5a   | Actor                                                        | System                  |
| ---- | ------------------------------------------------------------ | ----------------------- |
|      |                                                              | From Basic Flow step 4. |
| 1    | If the server can not receives the **RESPONSE** from the embedded system. The server resend the **REQUEST** as in Basic Flow step 1 for at most three times, if the server gets the **RESPONSE** from the embedded system, use case ends normally. There should be a 0.5-second interval between two **REQUESTs**. |                         |
| 2    | After three unsuccessful attempts, the server determines that the embedded system is unreachable, use case ends with exception. |                         |

**Post Conditions**

1. Users can obtain sensor status information, including sensor power after the Basic Flow ends.

**Supplemental Requirements**

None.

**Visual Model**

<img src="./UseCaseDiagram/Server Requests Sensor Status.svg" style="zoom:150%;" />

**Sequence Diagram**

![](./SequenceDiagram/RequestSensorStatus.svg)

**Revision History**

| Version | Date       | Author     | Description      | Status    |
| ------- | ---------- | ---------- | ---------------- | --------- |
| 1       | 2023-03-21 | Aidan, Bob | Original Version | Unaudited |

​		
## 4. Behavioral Requirements

### 4.1 System Inputs and Outputs
#### 4.1.1 Inputs
*暂时为空

#### 4.1.2 Outputs
*暂时为空

### 4.2 Detailed Output Behavior
*暂时为空

### 4.3 Quality Requirements
The data sampling rate does not exceed 5 frames / s.

## 5. Expected Subsets
*暂时为空

## 6. Fundamental Assumptions
*暂时为空

## 7. Expected Changes
*暂时为空

## 8. Appendices

### 8.1 Definitions and acronyms

#### 8.1.1 Definitions 

| Keyword | Definitions        |
| ------- | ------------------ |
| System  | The Embedded ystem |
|         |                    |
|         |                    |
|         |                    |

#### 8.1.2 Acronyms and abbreviations 

| Acronym or Abbreviation | Definitions |
| ----------------------- | ----------- |
|                         |             |
|                         |             |
|                         |             |

### 8.2 References

