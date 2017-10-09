#!/usr/bin/env python

import random
from twisted.internet import reactor,defer
from PyOPC.servers.basic import BasicXDAServer
from PyOPC.XDAServer import XDAServer
from PyOPC.XDAServer import ItemPairHolder
from PyOPC.utils import *
from PyOPC.OPCContainers import *

import pump_items

class WTCXDAServer(BasicXDAServer):
    OPCItems = pump_items.WTCOPCItems
    StatusInfo = 'Pump Items'

    def Browse(self, (IPH,inOptions,outOptions)):
        for key in self.OPCItemDict.keys():
            ReadItem = self.OPCItemDict.get(key, None)
            if ReadItem.getProperty('accessRights') and (ReadItem.getProperty('accessRights').Value != 'hidden' or ReadItem.getProperty('accessRights').Value != 'noAccess'):
                IPH.append(ItemContainer(),
                            ItemContainer(ItemName=key,
                                          IsItem = True,
                                          HasChildren = False))
        return XDAServer.Browse(self, (IPH, inOptions, outOptions))

    def Write(self, (IPH,inOptions,outOptions)):
		for inItem,outItem in IPH:
			key = mkItemKey(inItem)
			WriteItem = self.OPCItemDict.get(key, None)
			if WriteItem:
				accessRights = WriteItem.getProperty('accessRights')
				if accessRights and (accessRights.Value == 'readOnly' or accessRights.Value == 'noAccess'):
					outItem.IsEmpty = False
					outItem.ErrorText='Item is readOnly'
		return super(WTCXDAServer, self).Write((IPH,inOptions,outOptions))

if __name__ == '__main__':
    # Start the basic server
    from twisted.web import resource, server
    xdasrv = WTCXDAServer(http_log_fn = 'http.log')
    root = resource.Resource()
    root.putChild('',xdasrv)
    site = server.Site(root)
    reactor.listenTCP(8000, site)
    reactor.run()
