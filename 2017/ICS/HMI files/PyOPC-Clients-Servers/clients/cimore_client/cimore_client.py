#!/usr/bin/env python
from PyOPC.OPCContainers import *
from PyOPC.XDAClient import XDAClient
from config import paths
import time

def print_options((ilist,options)):
    print ilist; print options; print
    
cimore_address='http://127.0.0.1:8000'
relay1_address= paths['relay1']
relay2_address= paths['relay2']
gen1_address= paths['gen1']
gen2_address= paths['gen2']

cimore_xda = XDAClient(OPCServerAddress=cimore_address,ReturnErrorText=True)
relay1_xda = XDAClient(OPCServerAddress=relay1_address,ReturnErrorText=True)
relay2_xda = XDAClient(OPCServerAddress=relay2_address,ReturnErrorText=True)
gen1_xda = XDAClient(OPCServerAddress=gen1_address,ReturnErrorText=True)
gen2_xda = XDAClient(OPCServerAddress=gen2_address,ReturnErrorText=True)

while(True):
	try:
		relay1_breaker = int((relay1_xda.Read(ItemContainer(ItemName = "relay1_breaker")))[0][0].Value)
		gen1_generation = int((gen1_xda.Read(ItemContainer(ItemName = "gen1_generation")))[0][0].Value)
		gen1_breaker = int((gen1_xda.Read(ItemContainer(ItemName = "gen1_breaker")))[0][0].Value)
		relay1_load = int((cimore_xda.Read(ItemContainer(ItemName = "relay1_load")))[0][0].Value)

		relay2_breaker = int((relay2_xda.Read(ItemContainer(ItemName = "relay2_breaker")))[0][0].Value)
		gen2_generation = int((gen2_xda.Read(ItemContainer(ItemName = "gen2_generation")))[0][0].Value)
		gen2_breaker = int((gen2_xda.Read(ItemContainer(ItemName = "gen2_breaker")))[0][0].Value)
		relay2_load = int((cimore_xda.Read(ItemContainer(ItemName = "relay2_load")))[0][0].Value)
		power = 1
		if(gen1_breaker == 0 or relay1_breaker == 0):
			relay1_flow = 0
			power = 0
		else:
			if(gen1_generation < relay1_load):
				relay1_flow = gen1_generation
				power = 0
			else:
				relay1_flow = relay1_load

		if(gen2_breaker == 0 or relay2_breaker == 0):
			relay2_flow = 0
			power = 0
		else:
			if(gen2_generation < relay2_load):
				relay2_flow = gen2_generation
				power = 0
			else:
				relay2_flow = relay2_load
		cimore_xda.Write([ItemContainer(ItemName='power', Value=power)],LocaleID='en-us')

		cimore_xda.Write([ItemContainer(ItemName='relay1_flow', Value=relay1_flow)],LocaleID='en-us')
		cimore_xda.Write([ItemContainer(ItemName='relay1_breaker', Value=relay1_breaker)],LocaleID='en-us')
		cimore_xda.Write([ItemContainer(ItemName='gen1_generation', Value=gen1_generation)],LocaleID='en-us')
		cimore_xda.Write([ItemContainer(ItemName='gen1_breaker', Value=gen1_breaker)],LocaleID='en-us')
		relay1_xda.Write([ItemContainer(ItemName='relay1_flow', Value=relay1_flow)],LocaleID='en-us')
		relay1_xda.Write([ItemContainer(ItemName='relay1_load', Value=relay1_flow)],LocaleID='en-us')

		cimore_xda.Write([ItemContainer(ItemName='relay2_flow', Value=relay2_flow)],LocaleID='en-us')
		cimore_xda.Write([ItemContainer(ItemName='relay2_breaker', Value=relay2_breaker)],LocaleID='en-us')
		cimore_xda.Write([ItemContainer(ItemName='gen2_generation', Value=gen2_generation)],LocaleID='en-us')
		cimore_xda.Write([ItemContainer(ItemName='gen2_breaker', Value=gen2_breaker)],LocaleID='en-us')
		relay2_xda.Write([ItemContainer(ItemName='relay2_flow', Value=relay2_flow)],LocaleID='en-us')
		relay2_xda.Write([ItemContainer(ItemName='relay2_load', Value=relay2_load)],LocaleID='en-us')

		#pause for a bit
		time.sleep(4)
	except:
		time.sleep(4)
		continue
