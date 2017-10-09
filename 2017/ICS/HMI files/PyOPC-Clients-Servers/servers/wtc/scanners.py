from lib.Process import *
from PyOPC.XDAClient import *
from PyOPC.OPCContainers import *
import time,datetime,threading

class Scanner:
	def __init__(self, address='http://localhost:8000', name='TreatmentCenter', asset='tc_flow'):
		self.name = name
		self.pg = ProcessGroup(name, None, asset)
		icl = []
		self.state = True
		for skip,p in enumerate(self.pg.process_list):
			icl.append(ItemContainer(ItemName=p.name))

		self.xda_tc = XDAClient(OPCServerAddress=address)
		i,rd = self.xda_tc.Subscribe(icl, SubscriptionPingRate=200000)
		setattr(self.xda_tc, 'subhandle', rd['ServerSubHandle'])
		

	def UpdateTC(self):
		while True:
			status = {True : 'Online', False : 'Offline'}
			(inIClist, inOptions) = self.xda_tc.SubscriptionPolledRefresh(
                                                            ServerSubHandles=self.xda_tc.subhandle,
                                                            ReturnAllItems=False)
			print inIClist
			time.sleep(2)
			if inIClist:
				for skip,item in enumerate(inIClist):
					proc = self.pg.FindProcess(item.ItemName)
					if proc:
						proc.UpdateState(item.Value, self.xda_tc)
				self.state = self.pg.Online(self.xda_tc)

	def Status(self):
		return self.state

	def PrintState(self):
		print 'TREATMENT CENTER STATUS: ' + self.state

	def Start(self):
		self.tc_thread = threading.Thread(target=self.UpdateTC)
		self.tc_thread.daemon = True
		self.tc_thread.start()

class QualityScanner(Scanner):
	def __init__(self, address='http://localhost:8000', name='WaterQuality', asset='waterq', update_tag='H20_QUALITY'):
		self.name = name
		self.pg = QualityProcessGroup(name, None, asset)
		icl = []
		self.state = True
		self.update_tag = update_tag
		for skip,p in enumerate(self.pg.process_list):
			icl.append(ItemContainer(ItemName=p.name))

		self.xda_tc = XDAClient(OPCServerAddress=address)
		i,rd = self.xda_tc.Subscribe(icl, SubscriptionPingRate=200000)
		setattr(self.xda_tc, 'subhandle', rd['ServerSubHandle'])
	
	def UpdateTC(self):
		while True:
			status = {True : 'Online', False : 'Offline'}
			(inIClist, inOptions) = self.xda_tc.SubscriptionPolledRefresh(
                                                            ServerSubHandles=self.xda_tc.subhandle,
                                                            ReturnAllItems=False)

			time.sleep(.5)
			if inIClist:
				for skip,item in enumerate(inIClist):
					proc = self.pg.FindProcess(item.ItemName)
					if proc:
						proc.UpdateState(item.Value, self.xda_tc)
				self.state = self.pg.Online(self.xda_tc)
				self.xda_tc.Write([ItemContainer(ItemName=self.update_tag, Value=str(self.pg.Health()))])
