#!/usr/bin/env python
from PyOPC.OPCContainers import *
from PyOPC.XDAClient import XDAClient

def print_options((ilist,options)):
    print ilist; print options; print
    
address='http://192.168.1.51:8000/'

xda = XDAClient(OPCServerAddress=address,
                ReturnErrorText=True)

print_options(xda.Read([ItemContainer(ItemName='generation')]))
print_options(xda.Read([ItemContainer(ItemName='load')]))
print_options(xda.Read([ItemContainer(ItemName='breaker')]))
print_options(xda.Read([ItemContainer(ItemName='flow')]))
