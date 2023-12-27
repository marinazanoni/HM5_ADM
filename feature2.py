# feature2.py

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class GetFeature2:

    def __init__(self, graph, node, name):
        self.__graph = graph
        self.__node = node
        self.__name = name

    @property
    # Betweenness Centrality
    def nodecentrality(self):
        betweenness = nx.betweenness_centrality(self.__graph)
        return betweenness.get(self.__node,0)

    @property
    # PageRank Centrality
    def pagerank(self):
        pagerank = nx.pagerank(self.__graph)
        return pagerank.get(self.__node, 0)


    @property
    # Closeness Centrality
    def closeness(self):
        closeness = nx.closeness_centrality(self.__graph)
        return closeness.get(self.__node, 0)

    @property
    def degreecentrality(self):
         # Degree Centrality
        degree_centrality = nx.degree_centrality(self.__graph)
        return degree_centrality.get(self.__node, 0)




