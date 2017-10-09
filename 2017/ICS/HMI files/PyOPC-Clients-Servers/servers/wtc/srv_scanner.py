#!/usr/bin/env python

from lib.Process import *
from PyOPC.XDAClient import *
from PyOPC.OPCContainers import *
import time,datetime,threading
from scanners import Scanner,QualityScanner

def main():
	tc = Scanner()
	tc.Start()
	ps0 = Scanner(name='PS0', asset='ps_flow0')
	ps0.Start()
	ps1 = Scanner(name='PS1', asset='ps_flow1')
	ps1.Start()
	ps2 = Scanner(name='PS2', asset='ps_flow2')
	ps2.Start()
	ps3 = Scanner(name='PS3', asset='ps_flow3')
	ps3.Start()
	ps4 = Scanner(name='PS4', asset='ps_flow4')
	ps4.Start()
	ps5 = Scanner(name='PS5', asset='ps_flow5')
	ps5.Start()
	wq = QualityScanner(update_tag='H20_QUALITY')
	wq.Start()
	tc_thread = threading.Thread(target=NetworkStatus((tc,ps0,ps1,ps2,ps3,ps4,ps5,wq)))
	tc_thread.daemon = True
	tc_thread.start()

def NetworkStatus(net):
	while 1:	
		next = time.time()
		status = {True : 'Online', False : 'Offline'}
		for skip,item in enumerate(net):
			if isinstance(item, QualityScanner):
				print 'Water Quality: ' + str(item.pg.Health())
			else:
				print item.pg.name + ' STATUS: ' + status[item.Status()]
			
		next = next + 5
		time.sleep(next - time.time())
	
if __name__ == '__main__':
    main()
