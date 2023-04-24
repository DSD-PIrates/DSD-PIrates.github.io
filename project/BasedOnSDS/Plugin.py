def f(data:bytes)->None:
    assert len(data)==20
    (ox55,ox61,axL,axH,ayL,ayH,azL,azH,wxL,wxH,wyL,wyH,wzL,wzH,RollL,RollH,PitchL,PitchH,YawL,YawH)=data
    assert ox55==0x55
    assert ox61==0x61

    def int2(h:int,l:int)->int:
        ans=(h<<8)|l
        if ans>32767:
            ans-=65536
        return ans

    ax=int2(axH,axL)
    ay=int2(ayH,ayL)
    az=int2(azH,azL)
    wx=int2(wxH,wxL)
    wy=int2(wyH,wyL)
    wz=int2(wzH,wzL)
    Roll=int2(RollH,RollL)
    Pitch=int2(PitchH,PitchL)
    Yaw=int2(YawH,YawL)

    def linear(x:int,k:int)->float:
        return k*x/32768

    ax=linear(ax,16)
    ay=linear(ay,16)
    az=linear(az,16)
    wx=linear(wx,2000)
    wy=linear(wy,2000)
    wz=linear(wz,2000)
    Roll=linear(Roll,180)
    Pitch=linear(Pitch,180)
    Yaw=linear(Yaw,180)

    agx=ax
    agy=ay
    agz=az
    alx=0
    aly=0
    alz=0

    ret      = {
        "X"   : Roll, "Y"   : Pitch, "Z"   : Yaw,
        "accX": wx  , "accY": wy  , "accZ": wz,
        "asX" : ax  , "asY" : ay  , "asZ" : az
    }

    for term in ret:
        ret[term] = round(ret[term], 6)

    return ret
