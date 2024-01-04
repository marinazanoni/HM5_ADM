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

number_of_nodes = citation_graph.number_of_nodes()
number_of_edges = citation_graph.number_of_edges()

in_degrees = dict(citation_graph.in_degree())
out_degrees = dict(citation_graph.out_degree())

in_degree_values = list(in_degrees.values())
out_degree_values = list(out_degrees.values())

average_in_degree = sum(in_degree_values) / number_of_nodes
average_out_degree = sum(out_degree_values) / number_of_nodes

print(average_in_degree)
print(average_out_degree)

END
)

# Execute the Python code
python3 -c "$PYTHON_CODE"