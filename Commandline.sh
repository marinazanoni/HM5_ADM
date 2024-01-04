#!/bin/bash
# Code of program which finds what is the average length of the shortest path among nodes.

COM="import os\n\
import pandas as pd\n\
import numpy as np\n\
import networkx as nx\n\
import csv\n\
import json\n\
import numpy as np\n\
import networkx as nx\n\
from collections import deque\n\
from itertools import combinations\n\
\n\
with open('/home/alberto/Immagini/grafo.json', 'r') as file:\n\
    data = json.load(file)\n\
    G = nx.node_link_graph(data)\n\
\n\
shortestpl_sum = 0\n\
couple_nodes = list(combinations(G.nodes(), 2))\n\
for a, b in couple_nodes:\n\
    try:\n\
\t\tshortest_p = nx.shortest_path(G, a, b)\n\
\t\tshortestpl_sum += len(shortest_p)\n\
    except nx.NetworkXNoPath:\n\
        # Handle the case where there is no path between a and b\n\
\t\tpass\n\
\n\
avg_sp = shortestpl_sum / len(couple_nodes)\n\
print(avg_sp)"


echo -e $COM | python3
