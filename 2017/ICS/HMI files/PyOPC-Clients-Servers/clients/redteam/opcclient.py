#!/usr/bin/env python

from PyOPC.XDAClient import XDAClient
from PyOPC.OPCContainers import *
import argparse

def print_tags(tags):
	for skip, t in enumerate(tags):
		print t.ItemName + ' ' + str(t.Value)

parser = argparse.ArgumentParser('OPCClient')
group = parser.add_mutually_exclusive_group()
parser.add_argument('server', help='URL of OPC Server, e.g. http://localhost:8000')
group.add_argument('-b', '--browse', action='store_true', help='Browse OPC Server')
group.add_argument('-r', '--read', nargs=1, dest='read', metavar='TAG', help='Read a single tag from an OPC Server')
group.add_argument('-x', '--browseread', action='store_true', help='Read all tags at once from an OPC Server')
group.add_argument('-w', '--write', nargs=2, dest='write', metavar=('TAG', 'VALUE'), help='Write to an OPC Server')

args = parser.parse_args()

try:	
	xda = XDAClient(OPCServerAddress=args.server)
except:
	print 'Invalid server address, format is http://$SERVER:$PORT'
	exit()
	
if args.browse:
	print xda.Browse()
elif args.read:
	(stuff, junk) = xda.Read([ItemContainer(ItemName=args.read[0])])
	print_tags(stuff)
elif args.write:
	print 'Writing ' + args.write[0] + '=' + args.write[1] + ' to ' + args.server
	xda.Write([ItemContainer(ItemName=args.write[0], Value=args.write[1])])
elif args.browseread:
	(stuff, junk) = xda.Browse()
	(stuff, junk) = xda.Read(stuff)
	print_tags(stuff)
else:
	print 'Nothing to do'
