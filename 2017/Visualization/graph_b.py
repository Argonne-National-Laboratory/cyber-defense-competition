from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.io import output_notebook
output_notebook( resources=CDN )
import graph
import networkx as nx
import matplotlib.pyplot as plt

G = graph.G

pts = nx.circular_layout(G)
p = figure(
    x_range = (-.1,1.1),
    y_range = (-.1,1.1),
    height= 400,
    width= 400,
)
for edge in G.edges():
    p.line(
        x= [pts[pt][0] for pt in edge],
        y= [pts[pt][1] for pt in edge],
    )

for node in G.nodes():
    p.circle(
        x= [pts[node][0]],
        y= [pts[node][1]],
        radius=.05
    )
show(p)
