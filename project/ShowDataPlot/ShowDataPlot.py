import matplotlib.pyplot as plt
from Interface import getRealtimeData

timeIndex = []
xValue    = []
yValue    = []
zValue    = []

TIME_BUFFER = 25

SENSOR_ABS_NAME_LIST = ["R1"]
ATTR_PREFIX_LIST = ["", "acc", "as"]

def pushNewData(sensor_abstract_name, attr_prefix):
    global timeIndex
    global xValue
    global yValue
    global zValue

    ret = getRealtimeData()
    timestamp = ret["timestamp"]

    timeIndex.append(timestamp)
    xValue   .append(ret[sensor_abstract_name][attr_prefix + "X"])
    yValue   .append(ret[sensor_abstract_name][attr_prefix + "Y"])
    zValue   .append(ret[sensor_abstract_name][attr_prefix + "Z"])

    if len(timeIndex) > TIME_BUFFER:
        timeIndex = timeIndex[-TIME_BUFFER:]
        xValue = xValue[-TIME_BUFFER:]
        yValue = yValue[-TIME_BUFFER:]
        zValue = zValue[-TIME_BUFFER:]

def line_plot(abs_sensor_name, attr_prefix):
    plt.ion() # interactive ON
    while True:
        plt.cla()
        

        plt.title(attr_prefix + "X,Y,Z-" + abs_sensor_name)
        plt.grid(True)

        pushNewData(abs_sensor_name, attr_prefix)
        plt.ylim(-190, 190)
        plt.plot(timeIndex, xValue,'r-', label=attr_prefix + "X-" + abs_sensor_name)
        plt.plot(timeIndex, yValue,'g-', label=attr_prefix + "Y-" + abs_sensor_name)
        plt.plot(timeIndex, zValue,'b-', label=attr_prefix + "Z-" + abs_sensor_name)
        plt.legend()
        plt.pause(0.1)

line_plot("R1", "")