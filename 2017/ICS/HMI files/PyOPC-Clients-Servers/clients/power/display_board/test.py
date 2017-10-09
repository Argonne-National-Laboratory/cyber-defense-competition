#!/usr/bin/env python
from PyOPC.OPCContainers import *
from PyOPC.XDAClient import XDAClient

def print_options((ilist,options)):
    print ilist; print options; print
    
address='http://127.0.0.1:8000/'
#address='http://192.168.1.51:8000/'

xda = XDAClient(OPCServerAddress=address,
                ReturnErrorText=True)

#data = xda.Read([ItemContainer(ItemName='generation'),ItemContainer(ItemName='load'),ItemContainer(ItemName='breaker'),ItemContainer(ItemName='flow')])[0]
data = xda.Read([ItemContainer(ItemName='load')])[0]
print data[0].Value
#print data[1].Value
#print data[2].Value
#print data[3].Value


#print xda.Read([ItemContainer(ItemName='generation')])[0][0].Value
#print xda.Read([ItemContainer(ItemName='load')])[0][0].Value
#print xda.Read([ItemContainer(ItemName='breaker')])[0][0].Value
#print xda.Read([ItemContainer(ItemName='flow')])[0][0].Value
