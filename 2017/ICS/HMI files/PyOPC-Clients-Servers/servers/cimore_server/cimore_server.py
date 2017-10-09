#!/usr/bin/env python

from twisted.internet import reactor,defer
from cimore_BasicXDAServer import BasicXDAServer

# Read sample OPC items for testing
import cimore_items

class SimpleXDAServer(BasicXDAServer):
    OPCItems = cimore_items.OPCItems
    Ignore_ReturnItemPath=True
    Ignore_ReturnItemName=True

if __name__ == '__main__':
    # Start the basic server
    from twisted.web import resource, server
    xdasrv = SimpleXDAServer(http_log_fn = 0, access_log_fn = 0, error_log_fn = 0)
    root = resource.Resource()
    root.putChild('',xdasrv)
    site = server.Site(root)
    reactor.listenTCP(8000, site)
    reactor.run()
