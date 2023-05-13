import datetime
from time import sleep

tmp = datetime.datetime.now()
sleep(10)
print((datetime.datetime.now() - tmp).seconds / 60)