from itertools import combinations

from Levenshtein import distance
# import matplotlib.pyplot as plt

import networkx
g = networkx.Graph()

from socrata import columns
c = {k:v for k,v in columns() if len(v) > 10}

# Nodes
for k,v in c.items():
    g.add_node(k, { 'name': k[1], 'type': k[0], 'datasets': v })

# Edges
from random import sample
for low, high in combinations(c.keys(), 2):
    g.add_edge(low, high, { 'distance': distance(low[1], high[1]) })
