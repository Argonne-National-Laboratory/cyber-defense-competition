#!/usr/bin/env python
from PyOPC.OPCContainers import *
from PyOPC.XDAClient import XDAClient

def print_options((ilist,options)):
    print ilist; print options; print
    
address='http://192.168.1.51:8000/'

xda = XDAClient(OPCServerAddress=address,
                ReturnErrorText=True)

#print_options(xda.GetStatus())
#print_options(xda.Browse())
print_options(xda.Write([ItemContainer(ItemName='vat',Value=95)]))
