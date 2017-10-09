#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import PyOPC.XDAClient import XDAClient
import PyOPC.OPCContainers import *

GPIOPIN=4
ON=GPIO.LOW
OFF=GPIO.HIGH

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIOPIN, GPIO.OUT)

address='http://localhost:8000'

xda = XDAClient(OPCServerAddress=address)

(stuff, options) = xda.Browse()
(i,rd) = xda.Subscribe(stuff, SubscriptionPingRate=50000)
subhandle = rd['ServerSubHandle']

while True:
    try:
        (inIClist, inOptions) = xda.SubscriptionPollRefresh(ServerSubHandles=subhandle, ReturnAllItems=False)
        if inIClist:
            for skip, item in enumerate(inIClist):
                if item.Value == '1':
                    GPIO.output(GPIOPIN, ON)
                else:
                    GPIO.output(GPIOPIN, OFF)
    except:
        continue
