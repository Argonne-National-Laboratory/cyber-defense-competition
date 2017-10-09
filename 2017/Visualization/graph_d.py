#import networkx as nx
from NetworkxD3.NetworkxD3 import simpleNetworkx
from networkx.readwrite import d3_js
import graph
G = graph.G

simpleNetworkx(G)
#d3_js.export_d3_js(G, group="cdc")