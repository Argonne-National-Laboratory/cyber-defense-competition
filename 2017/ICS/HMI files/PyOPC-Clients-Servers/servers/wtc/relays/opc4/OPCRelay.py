#!/usr/bin/env python

import PyOPC.OpcXmlDaSrv_services as OPCSrv
from PyOPC.OPCContainers import *
from PyOPC.XDAServer import XDAServer
from PyOPC.XDAServer import ItemCache
from PyOPC.XDAServer import ItemPairHolder
from PyOPC.XDAClient import gen_operation
from PyOPC.servers.basic import BasicXDAServer
import copy,string,random,time,datetime,threading
import twisted
from twisted.python import log
from twisted.internet import reactor, defer

import relay_items

class OPCRelay(BasicXDAServer):

	OPCServerAddress = 'http://localhost:8000'
	SupportedLocaleIDs = ('en-us',)
	StatusInfo = 'OPC XML Server'
	ReturnItemPath = True
	ReturnItemName = True

	Relay_Browse = gen_operation('Browse')
	Relay_Read = gen_operation('Read')
	Relay_Subscribe = gen_operation('Subscribe')
	Relay_SubscriptionPolledRefresh = gen_operation('SubscriptionPolledRefresh')
	Relay_SubstrictionCancel =  gen_operation('SubscriptionCancel')
	Relay_Write = gen_operation('Write')

	OPCItems = relay_items.WTCOPCItems

	def __init__(self, *args, **kwargs):
		self.ReadCache = ItemCache(MaxAge=self.DefaultMaxAge)
		for key,value in kwargs.items():
			setattr(self, key, value)

		self._loc = OPCSrv.OpcXmlDaSrvLocator()

		self._portType = self._loc.getOpcXmlDaSrvSoap(self.OPCServerAddress,
													tracefile=file('soap_relay_requests.log', 'w'))
		random.seed()
		c = string.letters + string.digits
		s = ''.join([c[random.randint(0,len(c)-1)] for b in range(10)])
		self.ClientRequestHandle = 'ZSI_'+ s
		results = self.BuildSubscription(self.OPCItems)
		(inIClist, inOptions) = self.Relay_Read(results)
		(i,rd) = self.Relay_Subscribe(results, SubscriptionPingRate=10000)
		self.subhandle = rd['ServerSubHandle']
		self.OPCItemDict = self.mkItems(self.OPCItems)
		write_args = self.BuildOPCArgs(inIClist, inOptions)
		self.Self_Write(write_args)
		self.tmthread = threading.Thread(target=self.Refresh)
		self.tmthread.daemon = True
		self.tmthread.start()
		XDAServer.__init__(self, *args, **kwargs)

	def BuildSubscription(self, kl):
		icl = []
		for item,properties in kl:
			icl.append(item)
		return icl

	def mkItemsFromBrowse(self, kl):
		d = {}
		for skip,item in enumerate(kl):
			item.IsEmpty = False
			if hasattr(item, 'ClientItemHandle'):
				del(item.ClientItemHandle)
			d[mkItemKey(item)] = copy.deepcopy(item)
		return d

	def mkItemsFromRead(self, kl):
		d = {}
		for skip, item in enumerate(kl):
			ic = ItemContainer(ItemName=item.ItemName, IsItem=True, HasChildren = False)
			d[mkItemKey(ic)] = copy.deepcopy(ic)
		return d

	def BuildOPCArgs(self, inIClist, inOptions):
		IPH = ItemPairHolder()
		for inItem in inIClist:
			IPH.append(inItem=inItem, outItem=inItem)
		outOptions = {}
		return (IPH, inOptions, outOptions)

	def UnpackIPH(self, IPH):
		ic = []
		for inItem,outItem in IPH:
			ic.append(inItem)
		return ic

	def Self_Write(self, (IPH, inOptions, outOptions)):
		for inItem,outItem in IPH:
			if inItem.QualityField:
				del(inItem.QualityField)
			if inItem.VendorField:
				del(inItem.VendorField)
			if inItem.LimitField:
				del(inItem.LimitField)
			outItem.IsEmpty = True
		super(OPCRelay, self).Write((IPH, inOptions, outOptions))

	def Refresh(self):
		next = time.time()
		while True:
			(inIClist, inOptions) = self.Relay_SubscriptionPolledRefresh(
														ServerSubHandles=self.subhandle,
														ReturnAllItems=False)
			next = next + 2
			time.sleep(next - time.time())
			if inIClist:
				self.Self_Write(self.BuildOPCArgs(inIClist, inOptions))

	def Write(self, (IPH, inOptions, outOptions)):
		ic = self.UnpackIPH(IPH)
		(inIClist, inOptions) = self.Relay_Write(ic)
		return self.BuildOPCArgs(ic, inOptions)


if __name__=='__main__':
	from twisted.web import resource, server
	xdasrv = OPCRelay(http_log_fn='http.log')
	root = resource.Resource()
	root.putChild('',xdasrv)
	site = server.Site(root)
	reactor.listenTCP(8005, site)
	reactor.run()

