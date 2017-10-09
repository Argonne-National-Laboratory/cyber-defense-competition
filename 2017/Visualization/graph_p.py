import graph
import matplotlib.pyplot as plt
import networkx as nx
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

G = graph.G
a = 0.7

pos = graphviz_layout(G, prog='twopi', args='')
plt.figure(figsize=(8, 8))
#nx.draw_networkx_nodes(G,pos,node_size=700)
nx.draw_networkx_edges(G,pos,edgelist=graph.low, width=1, alpha=a)
nx.draw_networkx_edges(G,pos,edgelist=graph.lowmed, width=2, alpha=a)
nx.draw_networkx_edges(G,pos,edgelist=graph.med, width=3, edge_color="red", alpha=a)
nx.draw_networkx_edges(G,pos,edgelist=graph.himed, width=4, edge_color="red", alpha=a)
nx.draw_networkx_edges(G,pos,edgelist=graph.hi, width=6, edge_color="red", alpha=a)
#nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
nx.draw(G, pos, node_size=180, alpha=0.5, node_color="blue", with_labels=True)
plt.axis('equal')
plt.savefig('circular_tree.png')
plt.show()