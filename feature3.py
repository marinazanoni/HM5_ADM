import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import heapq
from sortedcontainers import SortedList

class CollaborationWalk:
    def __init__(self, graph, authors_publisheddf, listauthors, author1, authorn, N):
        """
        Initializes the CollaborationWalk class.

        Parameters:
        - graph: The collaboration graph (networkx graph).
        - authors_publisheddf: DataFrame containing information about authors.
        - listauthors: List of authors to consider.
        - author1: Starting author for collaboration.
        - authorn: Target author for collaboration.
        - N: Number of top authors to consider.
        """
        self.__graph = graph
        self.__listauthors = listauthors
        self.__author1 = author1
        self.__authorn = authorn
        self.N = N

    def extract(self):
        """
        Extracts a subgraph from the collaboration graph based on the top N authors.

        Returns:
        - subgraph: Subgraph containing collaboration information of top authors.
        """
        # Sort authors by publication count and extract top N authors
        new_df = authors_publisheddf.sort_values(by='PublicationCount', ascending=False)
        filtered_subgraph = new_df.head(self.N)

        # Find common nodes between the graph and the list of authors
        nodi_shared = set(self.__graph.nodes()).intersection(self.__listauthors)

        # Create a subgraph using common nodes
        subgraph = self.__graph.subgraph(nodi_shared)
        return subgraph

    def dijkstra(self, start, stop):
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
        distlist = {node: [float('inf'), []] for node in self.__graph}
        prev = {node: None for node in self.__graph.nodes}
        distlist[start][0] = 0
        alt = 0
        visited_nodes = SortedList([start])

        while min_heap:
            # Extract and process the node with the minimum distance
            u_dist, u = heapq.heappop(min_heap)

            # Iterate over neighbors of the current node
            for v, edge in self.__graph.adj[u].items():
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

    def connectauthor(self, authors_list=[]):
        """
        Connects authors based on the extracted subgraph and Dijkstra's algorithm.

        Parameters:
        - authors_list: List of intermediate authors to connect.

        Returns:
        - connected_path: List of nodes representing the connected path.
        """
        # Extract subgraph from top authors
        subgraph = self.extract()
        start = self.__author1
        stop = self.__authorn

        # Use Dijkstra's algorithm to find the path between start and stop
        if authors_list == []:
            connected_path = self.dijkstra(start, stop)
        else:
            connected_path = self.dijkstra(start, authors_list[0])

        # Handle cases where there is no path
        if connected_path[0] == float('inf'):
            print('There is no such path')
            return
        elif authors_list == []:
            return connected_path[1] + [stop]
        else:
            # Iterate over intermediate authors to connect them
            for i in range(1, len(authors_list)):
                connected_path_tmp = self.dijkstra(authors_list[i-1], authors_list[i])
                if connected_path[0] == float('inf'):
                    print('There is no such path')
                    return
                else:
                    connected_path[1].append(connected_path_tmp[1])

            # Connect the last intermediate author to the target author
            connected_path_tmp = self.dijkstra(authors_list[-1], stop)
            if connected_path_tmp[0] == float('inf'):
                print('The graph is not fully connected')
            else:
                return connected_path[1] + connected_path_tmp[1] + [stop]

        # Return an empty string in case of unexpected conditions
        return ""
