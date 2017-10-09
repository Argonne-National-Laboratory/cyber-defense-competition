#!/usr/bin/env python
from PyOPC.OPCContainers import *
from PyOPC.XDAClient import XDAClient

def print_options((ilist,options)):
    print ilist; print options; print
    
address='http://192.168.1.51:8000/'

xda = XDAClient(OPCServerAddress=address,
                ReturnErrorText=True)

print_options(xda.Write([ItemContainer(ItemName='breaker', Value=1)],
                       LocaleID='en-us'))
