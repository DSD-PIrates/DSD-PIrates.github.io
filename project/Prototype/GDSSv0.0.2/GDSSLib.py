# -*- encoding: utf-8 -*-

# GDSS v0.0.2
# Author: Bob

SPLIT_CHAR = "|" # can not be number, digit, +-=
COLUMN_SET = ["name", "data", "type"] # column set

import base64

def base64Encode(s: str):
    assert type(s) == str
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

def base64Decode(s: str):
    assert type(s) == str
    try:
        ans  = base64.b64decode(s.encode("utf-8")).decode("utf-8")
        flag = True
    except:
        ans  = ""
        flag = False # failed
    return ans, flag

def gdssDataChecker(data: dict):
    if type(data) != dict:
        return False, "gdssDataChecker: data type is not dict."
    for columnName in COLUMN_SET:
        if type(data.get(columnName)) != str:
            return False, "gdssDataChecker: data has no attr `%s`." % columnName
    for columnName in data:
        if columnName not in COLUMN_SET:
            return False, "gdssDataChecker: attr %s not in %s." % (columnName, COLUMN_SET)
    return True, "gdssDataChecker: test ok"

def gdssSerializer(data: dict):
    flag, errname = gdssDataChecker(data)
    if not flag: # can not pass gdssDataChecker
        raise AssertionError("data can not pass gdssDataChecker. [%s]" % errname)
    ans = ""
    for item in COLUMN_SET:
        ans += base64Encode(data[item]) + SPLIT_CHAR
    return ans[:-1] # delete the last split char

def gdssDeserializer(data: str):
    if type(data) != str:
        return False, "gdssDeserializer: data not str."
    dataSplit = data.split(SPLIT_CHAR)
    if len(dataSplit) != len(COLUMN_SET):
        return False, "gdssDeserializer: data length != len(COLUMN_SET)."
    ans = {}
    for index, b64code in enumerate(dataSplit):
        s, flag = base64Decode(b64code)
        if not flag:
            return False, "gdssDeserializer: decode b64 failed: %s" % b64code
        ans[COLUMN_SET[index]] = s
    return True, ans

if __name__ == "__main__":
    ser = gdssSerializer({
        "name": "hello",
        "type": "check",
        "data": "this is a test message."
    })
    print(ser)
    deser = gdssDeserializer(ser)
    print(deser)