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

  **Brief Introduction**

  Use trained model and data from Embedding, to calculate the status of equipment and GUI shows the result, until user stops

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed to Model mode

  **Basic Flow**

  |      | Actor                                   | System                  |
  | ---- | --------------------------------------- | ----------------------- |
  | 1    | User click "PredUserMotion_Sync" button |                         |
  | 2    |                                         | GUI shows the **[MotionRecord]**   |
  | 3    | User click "end" button                 |                         |
  | 4    |                                         | GUI releases connection |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 2.2  |       | If GUI receives error information, GUI shows the error notion, and back to Equip mode |
  | 2.3  |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |

  **Post Condition**

  GUI gets the result(the status of embedding)

- (2) Case: CollectData

  **Brief Introduction**

  GUI requests server to begin and end getting data, and Server takes charge of managing embedding, get and save data, save to DataBase.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into Equip mode

  **Basic Flow**

  |      | Actor                            | System                                                 |
  | ---- | -------------------------------- | ------------------------------------------------------ |
  | 1    | User click "Collect Data" button |                                                        |
  | 2    |                                  | GUI shows the **[MotionTag]**, and wait user to choose |
  | 3    | User choose one **[MotionTag]**  |                                                        |
  | 4    | User click "Finish Data" button  |                                                        |
  | 5    |                                  | GUI shows successful notion                            |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 5.2  |       | If GUI receives error information, GUI shows error notion and back to Equip mode |

  **Post Condition**

  Data has collected and saved to Data DataBase

#### 2.1.2 The secondary use cases

- (3) Case: Login

  **Brief Introduction**

  Allow user to log in the app and use functions.

  **Actors**

  Visitor

  **Pre-Conditions**

  The app is running.

  **Basic Flow**

  | Basic Flow | Actor                                     | System                    |
  | ---------- | ----------------------------------------- | ------------------------- |
  | 1          | User input **[AccountNumberAndPassword]** |                           |
  | 2          |                                           | Show an successful notion |
  | 3          |                                           | Change to user mode       |

  **Exception Flow**

  | Exception Flow | Actor | System                                                       |
  | -------------- | ----- | ------------------------------------------------------------ |
  |                |       | From basic flow 1                                            |
  | 4              |       | Inform visitor that he or she has input a **[AccountNumber]** that not exists or a wrong password. |

  **Post Conditions**

  The database has the user's information.

- (4) Case: Register

  **Brief Introduction**
  
  Register user
  
  **Actors**
  
  User
  
  **Pre-Conditions**
  
  GUI in visitor mode
  
  **Basic Flow**
  
  | Basic Flow | Actor                           | System                                                 |
  | ---------- | ------------------------------- | ------------------------------------------------------ |
  | 1          | User inputs **[AccountNumber]** |                                                        |
  | 2          |                                 | GUI checks whether **[AccountNumber]** is legal |
  | 3          | User inputs **[Password]** |                                                        |
  | 4          |                                 | GUI checks whether **[Password]** is legal     |
  | 5          | User reinputs **[Password]** |                                                        |
  | 6          |                                 | GUI checks whether the two **[Password]**s are same |
  | 7          | User inputs **[RegisterInformation]** escape **[AccountNumberAndPassword]** |                                                        |
  | 8          |                                 | GUI checks whether the **[RegisterInformation]** escape **[AccountNumberAndPassword]** is legal |
  | 9         |                                 | GUI shows successful notion and **[AccountNumber]** |
  
  **Exception Flow**
  
  | Exception Flow | Actor | System                                                       |
  | -------------- | ----- | ------------------------------------------------------------ |
  | 2.2            |       | If **[AccountNumber]** is not legal, shows mistake notion and back to step 1 |
  | 4.2            |       | If **[Password]** is not legal, shows mistake notion and back to step 3 |
  | 6.2            |       | If **[Password]** is different, shows mistake notion and back to step 5 |
  | 8.2            |       | If **[RegisterInformation]** escape **[AccountNumberAndPassword]** is not legal, shows mistake notion and back to step 7 |
  | 9.2            |       | If GUI receives error information(For example, the user has connected to one equip), GUI shows the error notion, and back to Equip mode |
  | 9.3            |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |
  
  **Post Conditions**
  
  User registered

- (5) Case:LogOut  

  **Brief Introduction**

  User log out

  **Actors**

  User

  **Pre-Conditions**

  A user has logged in the app.

  **Basic Flow**

  |      | Actor                           | System                       |
  | ---- | ------------------------------- | ---------------------------- |
  | 1    | User click the “log out” button |                              |
  | 2    |                                 | The app turn to visitor mode |

- (6) Case:UserInfo  

  **Brief Introduction**

  User choose to do something with personal information.and change to user information mode.

  **Actors**

  User

  **Pre-Conditions**

  A user has logged in the app.

  **Basic Flow**

  |      | Actor                                     | System                             |
  | ---- | ----------------------------------------- | ---------------------------------- |
  | 1    | User click the “User Information” button. |                                    |
  | 2    |                                           | Jump to User Information interface |

- (7) Case:GetPersonInfo  

  **Brief Introduction**

  Get the personal information set before.

  **Actors**

  User

  **Pre-Conditions**

  User choose the “user information” button.

  **Basic Flow**

  |      | Actor                                        | System                                          |
  | ---- | -------------------------------------------- | ----------------------------------------------- |
  | 1    | User choose to get **[AccountInformation]**. |                                                 |
  | 3    |                                              | Display **[AccountInformation]** on the screen. |



- (8) Case:SetPersonInfo  

  **Brief Introduction**

  Add personal information to database.

  **Actors**

  User

  **Pre-Conditions**

  User choose the “user information” button.

  **Basic Flow**

  |      | Actor                                        | System                               |
  | ---- | -------------------------------------------- | ------------------------------------ |
  | 1    | User choose to set **[AccountInformation]**. |                                      |
  | 2    | User input **[AccountInformation]**          |                                      |
  | 3    |                                              | Display successful notion on screen. |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 1    |       | The Exception Flow begins after step 3 of the main flow    |
  | 2    |       | The app informed the user that he or she has input invalid information. |

  **Post Conditions**

  New **[AccountInformation]** has been added to database.

- (9) Case:Equipment  

  **Brief Introduction**

  The user who have auxiliary walking tools choose to bind the tools with app to get better prediction.

  **Actors**

  User

  **Pre-Conditions**

  A user has logged in.

  **Basic Flow**

  |      | Actor                            | System                       |
  | ---- | -------------------------------- | ---------------------------- |
  | 1    | User click the equipment button. |                              |
  | 2    |                                  | Jump to equipment interface. |

- (10) Case:ConnectEquip  

  **Brief Introduction**

  User input the IP address and port of the equipment, and Server saved this to Equip DataBase.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into Equipment mode

  **Basic Flow**

  |      | Actor                                      | System                                                       |
  | ---- | ------------------------------------------ | ------------------------------------------------------------ |
  | 1    | User Click "ConnectEquip" button           |                                                              |
  | 2    |                                            | GUI shows the textbox, and wait user to input**[IPAddress]** and **[Port]** |
  | 3    | User inputs **[IPAddress]** and **[Port]** |                                                              |
  | 4    |                                            | GUI checks whether the input contents are legal and shows successful notion |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 4.2  |       | If the **[IPAddress]** or the [Port] is illegal, GUI shows the mistake notion, and back to step 3 |
  | 4.3  |       | If GUI receives error information(For example, the user has connected to one equip), GUI shows the error notion, and back to Equip mode |
  | 4.4  |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |

  **Post Conditions**

  Equipment saved to Equipment DataBase, and Server will charge of corresponding to Equipment

- (11) Case:GetEquipInfo  

  **Brief Introduction**

  GUI requests Server to give the Information of User's Equipment. Usually, Server needs to check the Embedding to get the Information.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into Equip mode

  **Basic Flow**

  |      | Actor                            | System                            |
  | ---- | -------------------------------- | --------------------------------- |
  | 1    | User Click "GetEquipInfo" button |                                   |
  | 2    |                                  | GUI shows **[DeviceInformation]** |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 6.2  |       | If GUI receives mistake information(For example, Server cannot connect the Equipment), GUI shows the mistake information and back to Equip mode |
  | 6.3  |       | If GUI receives error information, GUI shows the error notion, and back to Equip mode |
  | 6.4  |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |

  

- (12) Case:UnbindEquip  

  **Brief Introduction**

  GUI shows

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into Equip mode

  **Basic Flow**

  |      | Actor                                | System                         |
  | ---- | ------------------------------------ | ------------------------------ |
  | 1    | User clicks "UnbindEquip" button     |                                |
  | 2    |                                      | GUI shows the **[SensorList]** |
  | 3    | User chooses the Equipment to unbind |                                |
  | 4    |                                      | GUI shows successful notion    |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 2.2  |       | If there is no equipments on the user, show mistake notion and back to Equip mode |
  | 4.2  |       | If GUI receives error information, GUI shows the error notion, and back to Equip mode |
  | 4.3  |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |

  **Post Condition**

  Equipment of User is successfully unbinded



- (13) Case:GetEquipStatus 

  **Brief Introduction**

  GUI requests Server to give the Status of User's Equipments. Usually, Server needs to check the Embedding to get the Status.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into Equip mode

  **Basic Flow**

  |      | Actor                            | System                       |
  | ---- | -------------------------------- | ---------------------------- |
  | 1    | User Click "GetEquipInfo" button |                              |
  | 2    |                                  | GUI shows **[DeviceStatus]** |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 2.2  |       | If GUI receives mistake information(For example, Server cannot connect the Equipment), GUI shows the mistake information and back to Equip mode |
  | 2.3  |       | If GUI receives error information, GUI shows the error notion, and back to Equip mode |
  | 2.4  |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |

  **Post Condition**

  GUI gets the equipment information

- (14) Case:GetUserGuide  

  **Brief Introduction**

  User get the app's user guide

  **Actors**

  User

  **Pre-Conditions**

  A user has logged in. 

  **Basic Flow**

  |      | Actor                             | System                               |
  | ---- | --------------------------------- | ------------------------------------ |
  | 1    | The user choose to get user guide |                                      |
  | 2    |                                   | Get user guide and show it on screen |



- (15) Case:PredModel  

  **Brief Introduction**

  Change into model mode to get prediction results

  **Actors**

  User

  **Pre-Conditions**

  A user has logged in. 

  **Basic Flow**

  |      | Actor             | System                      |
  | ---- | ----------------- | --------------------------- |
  | 1    | User clicks Model |                             |
  | 2    |                   | GUI changes into model mode |

  **Post Condition**

  GUI changes into model mode



- (16) Case:ResetModel   

  **Brief Introduction**

  GUI requests Server to change the model of the user to initial model, whether the model of user is initial model or not.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into Model mode

  **Basic Flow**

  |      | Actor                           | System                      |
  | ---- | ------------------------------- | --------------------------- |
  | 1    | User clicks "ResetModel" button |                             |
  | 2    |                                 | GUI shows successful notion |

  **Exception Flow**

  |      | Actor | System                                                       |
  | ---- | ----- | ------------------------------------------------------------ |
  | 2.2  |       | If GUI receives error information, GUI shows the error notion, and back to Equip mode |
  | 2.3  |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |

  **Post Condition**

  The model of user resetted on his Algorithm database

- (17) Case:ShowModelInfo  

  **Brief Introduction**

  GUI gets information of model from server. Usually, server should get the information from algorithm database.

  **Actors**

  User

  **Pre-Conditions**

  User has changed into Model mode.

  **Basic Flow**

  | Basic Flow | Actor                             | System                        |
  | ---------- | --------------------------------- | ----------------------------- |
  | 1          | User click "ShowModelInfo" button |                               |
  | 2          |                                   | GUI shows the **[ModelInfo]** |
  

  **Exception Flow**

  | Exception Flow | Actor | System                                                       |
  | ---------------- | ----- | ------------------------------------------------------------ |
  | 2.2              |       | If GUI has not connected to Internet, GUI shows mistake information and back to Equip mode |
  | 2.3              |       | If GUI receives error information, GUI shows the error notion, and back to Equip mode |
  | 2.4              |       | If GUI waits more than time limitation, GUI shows the error notion, and back to Equip mode |

  **Post Conditions**

  none.

  **Supplemental Requirements**

  none.


- (18) Case:DataManagement  

  **Brief Introduction**

  Change into data mode to manage the collected data.

  **Actors**

  User

  **Pre-Conditions**

  User has log in.

  **Basic Flow**

  | Basic Flow | Actor                       | System                     |
  | ---------- | --------------------------- | -------------------------- |
  | 1          | User clicks Data management |                            |
  | 2          |                             | GUI changes into data mode |

  **Exception Flow**

  none.

  **Post Conditions**

  GUI changes into data mode.

  **Supplemental Requirements**

  none.


- (19) Case:GetData  

  **Brief Introduction**

  Get datalist from data DataBase.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into data mode.

  **Basic Flow**

  | Basic Flow | Actor                | System                       |
  | ---------- | -------------------- | ---------------------------- |
  | 1          | User clicks get data |                              |
  | 2          |                      | GUI shows **[MotionRecord]** |
  

**Exception Flow**

| Exception Flow | Actor | System                                                       |
  | ---------------- | ----- | ------------------------------------------------------------ |
  | 2.2              |       | If GUI cannot connect to Internet, shows mistake notion and back to data mode |

**Post Conditions**

GUI upload **[MotionRecord]** to database, and back into data mode.

**Supplemental Requirements**

none.


- (20) Case:DiscardData  

  **Brief Introduction**

  Get datalist from DataBase, and delete chosen data.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into data mode.

  **Basic Flow**

  | Basic Flow | Actor                       | System                       |
  | ---------- | --------------------------- | ---------------------------- |
  | 1          | User clicks get data        |                              |
  | 2          |                             | GUI shows **[MotionRecord]** |
  | 3          | User chooses data to delete |                              |
  | 4          |                             | GUI shows successful notion  |
  
  **Exception Flow**

  | Exception Flow | Actor | System                                                       |
  | ---------------- | ----- | ------------------------------------------------------------ |
  | 1.2              |       | If GUI cannot connect to Internet, shows mistake notion and back to data mode |
  | 2.2              |       | If nothing on datalist, GUI shows mistake notion and back to data mode |
  | 3.2              |       | If User chooses nothing or quit, GUI shows delete nothing and back to data mode |
  | 4.2              |       | If GUI cannot connect to Internet, shows mistake notion and back to data mode |
  
  **Post Conditions**

  Discard chosen data from data database, and GUI back into data mode.

  **Supplemental Requirements**

  none.


- (21) Case:ChangeDataLabel

  **Brief Introduction**

  Change the label of data in database.

  **Actors**

  User

  **Pre-Conditions**

  GUI has changed into data mode.

  **Basic Flow**

  | Basic Flow | Actor                                                        | System                      |
  | ---------- | ------------------------------------------------------------ | --------------------------- |
  | 1          | User clicks change label                                     |                             |
  | 2          |                                                              | GUI shows **[MotionTag]**   |
  | 3          | User chooses **[MotionTag]** to change, and chooses the new type |                             |
  | 4          |                                                              | GUI shows successful notion |
  
  **Exception Flow**

  | Alternative | Actor | System                                                       |
  | ----------- | ----- | ------------------------------------------------------------ |
  | 1.2         |       | If GUI cannot connect to Internet, shows mistake notion and back to data mode |
  | 2.2         |       | If nothing on datalist, GUI shows mistake notion and back to data mode |
  | 3.2         |       | If User chooses nothing, or the new type is the same as the old one, or quit, GUI shows alter nothing and back to data mode |
  | 4.2         |       | If GUI cannot connect to Internet, shows mistake notion and back to data mode |
  
  **Post Conditions**

  GUI upload data to data database, and back into data mode.

  **Supplemental Requirements**

  none.

### 2.2 User Stories for the User of **#WebApp#**
#### 2.2.1 Main user stories and corresponding main use cases

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

#### 2.2.2 The secondary use cases

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
|**[AccountNumber]:** A non-empty string consists of digits `"0-9"`, Latin letters `"a-z, A-Z"` and underscore `"_"`||
|**[Password]:** A non-empty string (The Android App SHOULD assure that the password is "legal" so that the other team will just regard it as a string.)||
|**[AccountNumberAndPassword]**=AccountNumber+Password||
|**[AccountInformation]**=AccountNumber+(PhoneNumber)+(EmailAddress)+(Birthday)||
|**[RegisterInformation]**=AccountNumber+Password+(PhoneNumber)+(EmailAddress)+(Birthday)||
|**[IPAddress]:** A string consists of digits and dot `"."`||
|**[Port]:** An integer not less than zero||
|**[DeviceIdentifier]**=IPAddress+Port||
|**[DeviceInformation]**=DeviceIdentifier+{SensorInformation}6||
|**[SensorList]**= {SensorInformation}6||
|**[SensorBattery]:** A non-negative integer which is not greater than 100||
|**[SensorOnlineStatus]:** An integer, `0` represents the sensor is offline, and `1` represents the sensor is online.||
|**[SensorStatus]**=SensorOnlineStatus+SensorBattery||
|**[DeviceStatus]**={SensorStatus}6||
|**[MotionTag]:** An integer, not less than zero and not greater than six.||
|**[Timestamp]**: An integer, milliseconds from `1970-01-01 00:00`||
|**[InitialTimestamp]:** A TimeStamp, to mark the begining time of a motion record.||
|**[MotionFrame]**={X+Y+Z+asX+asY+asZ+accX+accY+accZ}9+Timestamp|`X, Y, Z, asX, asY, asZ, accX, accY, accZ` are nine real numbers provided by the embedded system.|
|**[MotionRecord]**=AccountNumber+InitialTimestamp+MotionTag+{MotionFrame}||
|**[ModelInfo]**=modelflag+acc||