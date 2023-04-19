# Software Requirement Specification
[TOC]
## 1. Introduction

### 1.1 Compilatory Purpose
This ducument is compiled for 'Motion Prediction (MoPre)', which is a software system to predict the user's motion intention in the future time interval.

### 1.2 Ducument Conventions

- Every term between two sharp symbol "**#**" (like **#AndriodApp#**) can be found in section "Explanation of Terms" in the Appendix.
- Symbols in the Data Definitions
    - The plus operator "`[A]=B+C`" means Data `A` consists of Attribute `B` and Attribute `C`.

    - The brackets in `"(A)"` means Attribute `A` is an optional attribute (appears zero time or one time). 

    - The braces in `"{A}i"` means Attribute `A` will repeat in this data for exactly `i` times where `i` is an integer.

    - The braces (without an integer `i` after it) in `"{A}"`  means Attribute `A` will repeat for zero or more times.

### 1.3 Potential Readers
- Customer: User of **#AndroidApp#**, the one who uses a **#Device#** will login with the android app to collect data from the **#Device#**.
- System administrator: User of **#WebApp#**, the administrator will use the **#WebApp#** as a dashboard to check and **#ManageTheWholeSystem#**.
- Party A: The one who raised the target, played by Mr. Zhang.


### 1.4 Product Scope
The **#Software#** should have below functions.
- Track the motion of users using 6-axis sensors, bind to legs, to form a labeled dataset of human motions. These data are collected using Bluetooth; 
- Train a generalization model to predict human motions in general (via the dataset); 
- Provide a specialized model to predict the personal intention of a real-world user, with a relatively small number of new-coming motions tracked at run-time. 


### 1.5 References
- Concept of Operation
- The Requirement analysis document for **#AndroidAppTeam#**
- The Requirement analysis document for **#WebTeam#**

## 2. User Story

### 2.1 User Stories for the User of **#AndroidApp#**
#### 2.1.1 Main user stories and corresponding main use cases
The main purpose of the user of **#AndroidApp#** is listed as follows:

|User Story|Main Use Cases|
|-|-|
|As a **#Device#** user, I want to use model to give real-time predictions based on my current **#MotionData#**.|(1) Case: PredUserMotion|
|As a **#Device#** user, I want to record my **#MotionData#** into **[MotionRecord]**.|(2) Case: CollectData  |
|As a **#Device#** user, I want to acquire a trained model from my recorded **#MotionData#**.|*Included in (1) PredUserMotion, no user operation is required*|

The detailed description of the main use cases.

- (1) Case: PredUserMotion



- (2) Case: CollectData

#### 2.1.2 The secondary use cases

- (3) Case: Login



- (4) Case: Register


- (5) Case:LogOut  



- (6) Case:UserInfo  



- (7) Case:GetPersonInfo  



- (8) Case:SetPersonInfo  



- (9) Case:Equipment  



- (10) Case:ConnectEquip  



- (11) Case:GetEquipInfo  



- (12) Case:UnbindEquip  



- (13) Case:GetEquipStatus 



- (14) Case:GetUserGuide  



- (15) Case:PredModel  



- (16) Case:ResetModel   



- (17) Case:ShowModelInfo  


- (18) Case:DataManagement  


- (19) Case:GetData  


- (20) Case:DiscardData  


- (21) Case:ChangeDataLabel



### 2.2 User Stories for the User of **#WebApp#**
#### 2.1.1 Main user stories and corresponding main use cases
The main purpose of the user of **#WebApp#** is listed as follows:

|User Story|Main Use Cases|
|-|-|
|As an administrator of the **#Software#**, I want to view, modify the binding relationship between **#AndroidApp#** user and **#Device#**.|(1) Case: Administrators wants to view the list of Devices|
|As an administrator of the **#Software#**, I want to manage user information.|(2) Case: Administrators wants to manage users' information|
|As an administrator of the **#Software#**, I want to issue notifications.|(3) Case: Administrators wants to put a notice on the web site|

The detailed description of the main use cases.

- (1) Case: Administrators wants to view the list of Devices



- (2) Case: Administrators wants to manage users' information



- (3) Case: Administrators wants to put a notice on the web site
#### 2.1.2 The secondary use cases
- (4) Case: Adminstrators wants to view the historical data


- (5) Case: Administrator wants to manage the **#System#** log



## 3.Appendix

### 3.1 Explanation of Terms
|Term|Explanation|
|-|-|
|**#AndroidAppTeam#**| A synonym for "**Dreamweaver-GUI Team**".| 
|**#WebTeam#**|A synonym for "**mvps Team**".|
|**#CentralServer#**|The program created by "**genshin-impact-server team**", which is a **#ServerProgram#**.|
|**#Device#**|A raspberry pi with six sensors, each device will have a **FIXED** **[IPAddress]** and **[Port]** so that it can be accessed from the Internet if the device is powered on.|
|**#AndroidApp#**|An android application for the **#Device#** users.|
|**#ServerProgram#**|A program which will keep running 24hours a day.|
|**#RA#**|Short for "**Requirement Analysis**", which is a synonym for "**Software Requirement Specification**".|
|**#WebApp#**|A web site for the system administrator.|
|**#ManageTheWholeSystem#**|View, modify the binding relationship between users and devices, manage user information and issue notifications.|
|**#Software#**|Refer to the software system 'Motion Prediction (MoPre)'.|
|**#System#**|Same as **#Software#**|

### 3.2 Data Definitions
|Data Definitions|Tips|
|-|-|
|**[AccountNumber]:** A non-empty string consists of digits `"0-9"`, Latin letters `"a-z, A-Z"` and underscore `"_"`|
|**[Password]:** A non-empty string (The Android App SHOULD assure that the password is "legal" so that the other team will just regard it as a string.)|
|**[AccountNumberAndPassword]**=AccountNumber+Password|
|**[AccountInformation]**=AccountNumber+(PhoneNumber)+(EmailAddress)+(Birthday)|
|**[RegisterInformation]**=AccountNumber+Password+(PhoneNumber)+(EmailAddress)+(Birthday)|
|**[IPAddress]:** A string consists of digits and dot `"."`|
|**[Port]:** An integer not less than zero|
|**[DeviceIdentifier]**=IPAddress+Port|
|**[DeviceInformation]**=DeviceIdentifier+{SensorInformation}6|
|**[SensorBattery]:** A non-negative integer which is not greater than 100|
|**[SensorOnlineStatus]:** An integer, `0` represents the sensor is offline, and `1` represents the sensor is online.|
|**[SensorStatus]**=SensorOnlineStatus+SensorBattery|
|**[DeviceStatus]**={SensorStatus}6|
|**[MotionTag]:** An integer, not less than zero and not greater than six.|
|**[Timestamp]**: An integer, milliseconds from `1970-01-01 00:00`|
|**[InitialTimestamp]:** A TimeStamp, to mark the begining time of a motion record.|
|**[MotionFrame]**={X+Y+Z+asX+asY+asZ+accX+accY+accZ}9+Timestamp|`X, Y, Z, asX, asY, asZ, accX, accY, accZ` are nine real numbers provided by the embedded system.|
|**[MotionRecord]**=AccountNumber+InitialTimestamp+MotionTag+{MotionFrame}|