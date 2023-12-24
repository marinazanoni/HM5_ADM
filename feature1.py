# feature1.py

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class GetFeature1:

    def __init__(self, graph, name):
        self.__graph = graph
        self.__name = name

    @property
    def nnodes(self):
        return self.__graph.number_of_nodes()

    @property
    def nedges(self):
        return self.__graph.number_of_edges()

    @property
    def density(self):
        return nx.density(self.__graph)

    @property
    def degreedistr(self):
        # Calculate the degree distribution
        degree_sequence = [d for n, d in self.__graph.degree()]
        # Visualize it
        plt.hist(degree_sequence, bins=5, density=True, alpha=0.7)
        plt.show()  # Added to display the histogram

    @property
    def averagedegree(self):
        average_degree = 2 * self.__graph.number_of_edges() / self.__graph.number_of_nodes()
        return average_degree

    @property
    def hubs(self):
        # Create a dictionary with the number of nodes and the correspondence degree
        degrees = dict(self.__graph.degree())
        # Extracting only the values of the distribution to get the percentile
        degree_values = list(degrees.values())

        # Calculate the 95th percentile
        p95 = np.percentile(degree_values, 95)

        # Identify hubs (nodes with degrees > 95th percentile)
        hubs = [node for node, degree in degrees.items() if degree > p95]

        # Return the list of hubs (id are integers)
        return hubs

    @property
    def isdense(self):
        # Calculate the graph density using self
        density = self.density

        # Determine whether the graph is dense or sparse based on a threshold
        nnodes = self.nnodes
        Emax = nnodes * (nnodes - 1) // 2
        # We consider 0.6 as typically NOT dense graph has really lower number of edges r.t.w. the maximum number of edges. We also like this assessment as we consider it logical
        if density >= 0.6 * Emax:
            # Whether a graph is dense
            return True
        else:
            # If a graph is NOT dense
            return False
