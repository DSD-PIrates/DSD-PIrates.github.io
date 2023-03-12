
DATA_ATTR = ['accX', 'accY', 'accZ', 'asX', 'asY', 'asZ', 'angleX', 'angleY', 'angleZ', 'time']

def MyDumpData(data):
    assert type(data) == dict
    lis = []
    for x in DATA_ATTR:
        assert data.get(x) is not None
        lis.append(str(data.get(x)))
    return ":".join(lis)

def MyDumps(dic: dict):
    assert type(dic) == dict
    assert dic.get("name") is not None
    assert dic.get("type") is not None
    assert dic.get("data") is not None
    assert dic.get("hash") is not None
    return ":".join([
        str(dic["name"]),
        str(dic["type"]),
        str(MyDumpData(dic["data"])),
        str(dic["hash"])
    ])
