from itertools import combinations

from Levenshtein import distance
# import matplotlib.pyplot as plt

import networkx
g = networkx.Graph()

from socrata import columns
c = columns()

# Nodes
for k,v in c.items():
    g.add_node('\n'.join(k), { 'name': k[1], 'type': k[0], 'datasets': v })

# Edges
from random import sample
for low, high in combinations(sample(c.keys(), 100), 2):
    # If they're of similar length,
    if (len(low[1]) - len(high[1])) / (len(low[1]) + len(high[1])) < (1/3):
        # add the edge.
        g.add_edge('\n'.join(low), '\n'.join(high), { 'distance': distance(low[1], high[1]) })
