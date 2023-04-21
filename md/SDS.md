


# Software Design Specification (SDS)

Revision History: 

| Date      | Author | Description |
| ----      | ------ | ----------- |
| Apr 10   | Zin, Bob | First version |

<style>#rev +table td:nth-child(1) { white-space: nowrap }</style>
<div id="rev"></div>

[toc]

## 1. Introduction

### 1.1 Intended Audience and Purpose

The document is intended to help the customer understand the system design, and serves as the basis of task division and inter-module communication, providing design information for developers and testers.

### 1.2 How to use the document

The document is organized as follows:

- show the system design of embedded system module
- show the detailed design of  modules


## 2. System Design
### 2.1 Context

- The embedded system module is divided in three part. The first part is the Router to respond to the requests from the server. The second part is four function components. They are called by Router to complete requests. The last part is DataCollector. It serves as a medium for interacting with sensors.
- The embedded system is planned to develop with python

### 2.2 Architecture
#### 2.2.1 Component Diagram
- version 1.0

![component](./component.png)



## 3. Detailed Design

### 3.1 Class Diagram

version 1.0

![class](./class.png)



### 3.2 Class Design



#### 3.2.1 `Router`

##### `Attribute`

```
IP: string		
```

The IP of server

```
Port: int
```

```
transactionlist: list
```

The list of objects for processing requests.

##### `Operation`

```
Router.getResponse(dataInput: dict): dict
```

Call different functions of different objects in `transactionlist` according to `dataInput` to process server requests.

Return `dict` always.

```
Router.start(): void
```

Start sensor clients to connect with sensors. And start http server to  wait and process server requests.

Return `None` always.



#### 3.2.2 `Transaction`

##### `Attribute`

```
collectorlist: list
```

A list of SensorCollector objects.

##### `Operation`

```
Transaction.getResponse(): dict
```

Process requests received by Router.

Return `dict` always. 

```
Transaction.checkSuitable(dataInput: dict): bool
```

Check if the request type matches the current object.

Return `true` if match successfully,  `false` otherwise.



#### 3.2.3 `RealTimeData`

##### `Attribute`

##### `Operation`

```
RealTimeData.getResponse(): dict
```

Call `SensorCollector.getRealtimeData()` to request real-time data from sensors.

Return `dict` always.

```
RealTimeData.checkSuitable(): bool
```

Check if the request matches the type of request that can be processed

Return `true` if match successfully,  `false` otherwise.



#### 3.2.4 `SensorStatus`

##### `Attribute`

##### `Operation`

```
SensorStatus.getResponse(): dict
```

Call `SensorCollector.getSensorStatus()` to request sensor status information from sensors.

Return `dict` always.

```
SensorStatus.checkSuitable(): bool
```

Check if the request matches the type of request that can be processed

Return `true` if match successfully,  `false` otherwise.



#### 3.2.5 `SensorDetails`

##### `Attribute`

##### `Operation`

```
SensorDetails.getResponse(): dict
```

Get the sensors detail.

Return `dict` always.

```
SensorDetails.checkSuitable(): bool
```

Check if the request matches the type of request that can be processed

Return `true` if match successfully,  `false` otherwise.



#### 3.2.6 `SensorCalibration`

##### `Attribute`

##### `Operation`

```
SensorCalibration.getResponse(): dict
```

Call `SensorCollector.calibrateSensor()` to perform sensors calibration.

Return `dict` always.

```
SensorCalibration.checkSuitable(): bool
```

Check if the request matches the type of request that can be processed

Return `true` if match successfully,  `false` otherwise.



#### 3.2.7 `SensorCollector`

##### `Attribute`

```
datatranform: DataTranform
```

A object which can call `transformData()` to transform data.

```
Mac: string
```

The Mac of sensor.

##### `Operation`

```
SensorCollector.getRealtimeData(): dict
```

Request real-time data from sensors and then call `DataTransform.transformData()` to transform the format of data.

Return `dict` always.

```
SensorCollector.getSensorStatus(): dict
```

Request request sensor status information from sensors and then call `DataTransform.transformData()` to transform the format of data.

Return `dict` always.

```
SensorCollector.calibrate(): dict
```

Perform sensors calibration.

Return `dict` always.

```
SensorCollector.start(): void
```

Connect with sensor, request data from sensor and check if connection is maintained, if not, reconnect with sensor.

Return `None` always.



#### 3.2.8 `DataTransform`

##### `Attribute`

##### `Operation`

```
DataTransform.transformData(originData: dytes, type: string): dict
```

Transform the format of data from `dytes` to `double`.

Return `dict` always.
