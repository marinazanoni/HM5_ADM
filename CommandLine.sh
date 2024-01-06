#Preliminar activities
# Python code to be executed
PYTHON_CODE=$(cat <<-END

import pickle
import networkx as nx
import pandas as pd


with open('citation_graph.pickle', 'rb') as f:
    citation_graph = pickle.load(f)


# Point 4.1
# we decided to solve the first question of the Command Line question using the 'betweeness centrality' as a easure of the centrailty of a node inside the graph
betweeness_centrality = nx.betweenness_centrality(citation_graph)

df = pd.DataFrame(list(betweeness_centrality.items()), columns=['Node', 'Betweenness_Centrality'])

df.to_csv('centrality_scores.csv', index=False)

dataframe_centrality_scores = pd.read_csv('centrality_scores.csv')

min_score = dataframe_centrality_scores['Betweenness_Centrality'].min()
max_score = dataframe_centrality_scores['Betweenness_Centrality'].max()
dataframe_centrality_scores['Normalized_Betweenness'] = (dataframe_centrality_scores['Betweenness_Centrality'] - min_score) / (max_score - min_score)

df_sorted = dataframe_centrality_scores.sort_values(by='Normalized_Betweenness', ascending=False)
print(df_sorted)

df_sorted_by_betweenness = dataframe_centrality_scores.sort_values(by='Betweenness_Centrality', ascending=False)
top_nodes_betweenness = df_sorted_by_betweenness.head(10)

print(top_nodes_betweenness[['Node', 'Betweenness_Centrality']])


#Point 4.2
END
)

# Execute the Python code
python3 -c "$PYTHON_CODE"
g_citation='g_citation.csv'
awk -F',' 'NR > 1 {count[$2]++} END {
    total = 0
    for (node in count) {
        total += count[node]
        }
    average = total / length(count)
    print "average in degree: " average
}' "$g_citation"

# Calculate out-degree statistics
awk -F',' 'NR > 1 {count[$1]++} END {
    total = 0
    for (node in count) {
        total += count[node]
        }
    average = total / length(count)
    print "average out degree: " average
}' "$g_citation"


#Point 4.3


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
with open('/home/oem/ADM5/grafo.json', 'r') as file:\n\
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
