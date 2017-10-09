#!/usr/bin/env python
import time
from PyOPC.OPCContainers import *
from PyOPC.XDAClient import XDAClient
from config import paths

def print_options((ilist,options)):
    print ilist; print options; print
    
cimore_address='http://127.0.0.1:8000/'
display_address= paths['display_board']

cimore_xda = XDAClient(OPCServerAddress=cimore_address,ReturnErrorText=True)
display_xda = XDAClient(OPCServerAddress=display_address,ReturnErrorText=True)
num_lights = 7

while(True):

	try:
		data1 = cimore_xda.Read([ItemContainer(ItemName='generation')])[0]
		data2 = cimore_xda.Read([ItemContainer(ItemName='load')])[0]
		data3 = cimore_xda.Read([ItemContainer(ItemName='breaker')])[0]
		data4 = cimore_xda.Read([ItemContainer(ItemName='flow')])[0]
		gen = float(data1[0].Value)
		load = float(data2[0].Value)
		breaker = int(data3[0].Value)
		flow = float(data4[0].Value)
		
		per_served = flow / load
		
		if(per_served >= 1):
			n = 6
		elif(per_served > .833):
			n = 5
		elif(per_served > .666):
			n = 4
		elif(per_served > .5):
			n = 3
		elif(per_served > .333):
			n = 2
		elif(per_served > .166):
			n = 1
		else:
			n = 0
	
	
		if(n != num_lights):
			if(per_served >= 1):
				display_xda.Write([ItemContainer(ItemName='a', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='b', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='c', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='d', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='e', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='f', Value='1')],LocaleID='en-us')
			elif(per_served > .833):
				display_xda.Write([ItemContainer(ItemName='a', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='b', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='c', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='d', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='e', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='f', Value='0')],LocaleID='en-us')
			elif(per_served > .666):
				display_xda.Write([ItemContainer(ItemName='a', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='b', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='c', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='d', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='e', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='f', Value='0')],LocaleID='en-us')
			elif(per_served > .5):
				display_xda.Write([ItemContainer(ItemName='a', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='b', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='c', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='d', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='e', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='f', Value='0')],LocaleID='en-us')
			elif(per_served > .333):
				display_xda.Write([ItemContainer(ItemName='a', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='b', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='c', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='d', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='e', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='f', Value='0')],LocaleID='en-us')
			elif(per_served > .166):
				display_xda.Write([ItemContainer(ItemName='a', Value='1')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='b', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='c', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='d', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='e', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='f', Value='0')],LocaleID='en-us')
			else:
				display_xda.Write([ItemContainer(ItemName='a', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='b', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='c', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='d', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='e', Value='0')],LocaleID='en-us')
				display_xda.Write([ItemContainer(ItemName='f', Value='0')],LocaleID='en-us')
		num_lights = n
		time.sleep()
	except:
		time.sleep(4)
		continue

