#!/usr/bin/env python
from PyOPC.OPCContainers import *
from PyOPC.XDAClient import XDAClient

def print_options((ilist,options)):
#    print ilist
    for skip,x in enumerate(ilist):
	print x.ItemName; print x.Value; print

#address='http://192.168.122.153:8001/'
address='http://localhost:8000'
#address='http://192.168.122.82:8001'
#address='http://192.168.122.224:8002'

xda = XDAClient(OPCServerAddress=address,
                ReturnErrorText=True)

print_options(xda.GetStatus())
(stuff, options) = xda.Browse()
#print stuff
icl = []
icl.append(stuff[3])
icl.append(stuff[2])
icl.append(stuff[1])
icl.append(stuff[0])

print_options(xda.Read([ItemContainer(ItemName='PS0_DEST_NET', MaxAge=500)],
                      LocaleID='en-us'))
print_options(xda.Read([ItemContainer(ItemName='PS5_CHLOR', MaxAge=500), ItemContainer(ItemName='PS0_VALVE_1',)],
                       LocaleID='en-us'))

print_options(xda.Read([ItemContainer(ItemName='PS0_PUMP_1', MaxAge=500)],
                       LocaleID='en-us'))
print_options(xda.Read(stuff, MaxAge=0))
print_options(xda.Read(icl))
