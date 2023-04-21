import random
import time

def solve(jsonData: dict):
    # check type == dict
    if type(jsonData) is not dict:
         return {
            "type"   : "Error",
            "message": "RequestObjectIsNotJson"
        }
    # calculate and get the response value
    if type(jsonData.get("type")) == str:
        # TODO: add interface functions here
        if   jsonData.get("type") == "Ping"             : return getPingResponse          (jsonData)
        elif jsonData.get("type") == "GetRealtimeData"  : return getRealtimeDataResponse  (jsonData)
        elif jsonData.get("type") == "GetSensorStatus"  : return getSensorStatusResponse  (jsonData)
        elif jsonData.get("type") == "SensorCalibration": return sensorCalibrationResponse(jsonData)
        elif jsonData.get("type") == "GetSensorDetails" : return getSensorDetailsResponse (jsonData)
        else:
            return {
                "type"   : "Error",
                "message": "RequestTypeUnknown",
                "details": str(jsonData.get("type"))
            }
    else:
        return {
            "type"   : "Error",
            "message": "AttrTypeUndefined" # fixed
        }

def getPingResponse(jsonData: dict):
    return {
        "type"   : "PingResponse",
        "message": "ConnectToEmbeddedSystemSuccessfully" # fixed
    }

def makeMesage(tp:str, msg: str):
    return {
        "type": str(tp), "message": str(msg),
    }

def translateNone(v) -> str:
    if v is None: return ""
    else:         return str(v)

def getTimeNow():
    return time.time() * 1000

def getRealtimeDataResponse(jsonData: dict):
    return {
        "type": "GetRealtimeDataResponse",
        "timestamp": getTimeNow(),
        "L1":{
            "X"   : 0.0, "Y"   : 0.0, "Z"   : 0.0,
            "accX": 0.0, "accY": 0.0, "accZ": 0.0,
            "asX" : 0.0, "asY" : 0.0, "asZ" : 0.0
        },
        "L2":{
            "X"   : 0.0, "Y"   : 0.0, "Z"   : 0.0,
            "accX": 0.0, "accY": 0.0, "accZ": 0.0,
            "asX" : 0.0, "asY" : 0.0, "asZ" : 0.0
        },
        "L3":{
            "X"   : 0.0, "Y"   : 0.0, "Z"   : 0.0,
            "accX": 0.0, "accY": 0.0, "accZ": 0.0,
            "asX" : 0.0, "asY" : 0.0, "asZ" : 0.0
        },
        "R1":{
            "X"   : 0.0, "Y"   : 0.0, "Z"   : 0.0,
            "accX": 0.0, "accY": 0.0, "accZ": 0.0,
            "asX" : 0.0, "asY" : 0.0, "asZ" : 0.0
        },
        "R2":{
            "X"   : 0.0, "Y"   : 0.0, "Z"   : 0.0,
            "accX": 0.0, "accY": 0.0, "accZ": 0.0,
            "asX" : 0.0, "asY" : 0.0, "asZ" : 0.0
        },
        "R3":{
            "X"   : 0.0, "Y"   : 0.0, "Z"   : 0.0,
            "accX": 0.0, "accY": 0.0, "accZ": 0.0,
            "asX" : 0.0, "asY" : 0.0, "asZ" : 0.0
        }
    }

def getSensorStatusResponse(jsonData: dict):
    return {
        "type": "GetSensorStatusResponse",
        "L1":{
            "connect": True,
            "battery": 100
        },
        "L2":{
            "connect": True,
            "battery": 100
        },
        "L3":{
            "connect": True,
            "battery": 100
        },
        "R1":{
            "connect": True,
            "battery": 100
        },
        "R2":{
            "connect": True,
            "battery": 100
        },
        "R3":{
            "connect": True,
            "battery": 100
        }
    }

def sensorCalibrationResponse(jsonData: dict):
    chance = random.randint(1, 10)
    if chance <= 1:
        return {
            "type":"CalibrationFailure"
        }
    else:
        return {
            "type":"CalibrationSuccess"
        }
    
def getSensorDetailsResponse(jsonData: dict):
    return {
        "type": "GetSensorDetailsResponse",
        "L1":{
            "name": "WT901-DEMO-XX",
            "macAddr": "XX:XX:XX:XX:XX:XX"
        },
        "L2":{
            "name": "WT901-DEMO-XX",
            "macAddr": "XX:XX:XX:XX:XX:XX"
        },
        "L3":{
            "name": "WT901-DEMO-XX",
            "macAddr": "XX:XX:XX:XX:XX:XX"
        },
        "R1":{
            "name": "WT901-DEMO-XX",
            "macAddr": "XX:XX:XX:XX:XX:XX"
        },
        "R2":{
            "name": "WT901-DEMO-XX",
            "macAddr": "XX:XX:XX:XX:XX:XX"
        },
        "R3":{
            "name": "WT901-DEMO-XX",
            "macAddr": "XX:XX:XX:XX:XX:XX"
        }
    }
