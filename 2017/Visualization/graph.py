import networkx as nx
import matplotlib.pyplot as plt
import random

try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydotplus
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or PyDotPlus")

G = nx.Graph()
import config
root = "10.10.20.1"
G.add_node(root)
for t in config.cdc:
    G.add_node(t["name"])
    G.add_edge(root, t["name"])
    for serv, last_oct in config.blue.items():
        ip = "%s.%s" % (config.getPrefix(t["num"]), last_oct)
        G.add_node(ip)
        G.add_edge(t["name"], ip)
        G[t["name"]][ip]['weight'] = random.randint(0, 1000)
    G[root][t["name"]]['weight'] = random.randint(0, 1000)


thresholds = [1000,1500,2000,2500]

low=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] < thresholds[0]]
lowmed=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] in range(thresholds[0], thresholds[1])]
med=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] in range(thresholds[1], thresholds[2])]
himed=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] in range(thresholds[2], thresholds[3])]
hi=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] > thresholds[3]]
