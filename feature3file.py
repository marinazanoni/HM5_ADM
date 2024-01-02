import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heapq
from sortedcontainers import SortedList



path_csv = '/media/alberto/STORE N GO/cartellaprovvisorio/authors_publisheddf.csv'

# Leggi il file CSV e assegna i dati a un DataFrame
authors_publisheddf = pd.read_csv(path_csv)

#Extracts a subgraph from the collaboration graph based on the top N authors.
#Returns a subgraph: Subgraph containing collaboration information of top authors.
# Sort authors by publication count and extract top N authors

def extract(graph, N=150):
    # Sort the dataset such that we have the top authors
    new_df = authors_publisheddf.sort_values(by='PublicationCount', ascending=False)
    # Select the top-N authors
    filtered_data = new_df.head(N)

    #We consider the subgraph of the first one with the node from the list in the
    #variable id of new_df and within the original graph
    listauth= filtered_data['id'].tolist()

    # Create a subgraph using common nodes (nx handles appropriatly when some nodes are not
    #met in the original graph from which I want to subset)
    subgr = graph.subgraph(listauth)

    return subgr



def dijkstra(graph, start, stop):
    """
    Applies Dijkstra's algorithm to find the shortest path between two nodes in the graph.

    Parameters:
    - start: Starting node.
    - stop: Target node.

    Returns:
    - distlist[stop]: List of nodes representing the shortest path.
    """
    # Initialize priority queue and distance lists
    min_heap = [(0, start)]
    heapq.heapify(min_heap)
    distlist = {node: [float('inf'), []] for node in graph}
    prev = {node: None for node in graph.nodes}
    distlist[start][0] = 0
    alt = 0
    visited_nodes = SortedList([start])

    while min_heap:
        # Extract and process the node with the minimum distance
        u_dist, u = heapq.heappop(min_heap)

        # Iterate over neighbors of the current node
        for v, edge in graph.adj[u].items():
            alt = distlist[u][0] + edge['weight']
            if alt < distlist[v][0]:
                # Update distance and path if a shorter path is found
                prev[v] = u
                if v in visited_nodes:
                    min_heap.remove((distlist[v][0], v))
                else:
                    visited_nodes.add(v)
                heapq.heappush(min_heap, (alt, v))
                distlist[v][0] = alt
                distlist[v][1] = distlist[u][1] + [u]

        # Return the shortest path to the target node
    return distlist[stop]




def connectauthor(graph, start, stop, N=150, authors_list=[]):
    """
    Connects authors based on the extracted subgraph and Dijkstra's algorithm.

    Parameters:
    - authors_list: List of intermediate authors to connect.

    Returns:
    - connected_path: List of nodes representing the connected path.
    """
    # Extract subgraph from top authors
    #subres = extract(G_collaboration, N)

    # Use Dijkstra's algorithm to find the path between start and stop
    if authors_list == []:
        connected_path = dijkstra(graph, start, stop)
    else:
        connected_path = dijkstra(graph, start, authors_list[0])

    # Handle cases where there is no path
    if connected_path[0] == float('inf'):
        print('There is no such path')
        return
    elif authors_list == []:
        return connected_path[1] + [stop]
    else:
        # Iterate over intermediate authors to connect them
        for i in range(1, len(authors_list)):
            connected_path_tmp = dijkstra(graph, authors_list[i-1], authors_list[i])
            if connected_path[0] == float('inf'):
                print('There is no such path')
                return
            else:
                connected_path[1].append(connected_path_tmp[1])

        # Connect the last intermediate author to the target author
        connected_path_tmp = dijkstra(graph, authors_list[-1], stop)
        if connected_path_tmp[0] == float('inf'):
            print('The graph is not fully connected')
        else:
            return connected_path[1] + connected_path_tmp[1] + [stop]

    # Return an empty string in case of unexpected conditions
    return ""
