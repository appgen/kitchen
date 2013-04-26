from itertools import combinations

from Levenshtein import distance

import networkx
g = networkx.Graph()

from socrata import columns
c = columns()

# Nodes
for k,v in c.items():
    g.add_node(k, { 'datasets': v })

# Edges
for low, high in combinations(c.keys(), 2):
    g.add_edge(low, high, { 'distance': distance(low, high) })
