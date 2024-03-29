import networkx as nx
import matplotlib.pyplot as plt


def functionality5(G, N, paper1, paper2):
    '''
    G is the graph data
    N are the top N papers that their data should be considered
    Paper_1: denoting the name of one of the papers
    Paper_2: denoting the name of one of the papers
    '''
    # Make a copy of the graph
    G=G.copy()
    # Convert the directed graph to undirected
    G_undirected = G.to_undirected()

    degree_centrality = nx.degree_centrality(G_undirected)
    top_N_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:N]

    G_N = G_undirected.subgraph(top_N_nodes)

    e_b = nx.edge_betweenness_centrality(G_N)
    sorted_edges = sorted(e_b.items(), key=lambda x: x[1], reverse=True)
    
    def girvan_newman(graph, sorted_edges):
        edges_start = len(sorted_edges)
        sg = nx.connected_components(graph)
        sg_count = nx.number_connected_components(graph)

        while(sg_count == 1):
            #get the edge to remove from the graph and delate it from the list of edges
            which_edge = sorted_edges.pop(0)[0]
            #remove the edge from the graph
            graph.remove_edge(*which_edge)
            sg = nx.connected_components(graph)
            sg_count = nx.number_connected_components(graph)
        edges_end = len(sorted_edges)
        min_edges_removed = edges_start - edges_end    
        return sg, min_edges_removed

    connected, min_edges_removed = girvan_newman(G_N, sorted_edges)
    communities = []

    for i in connected:
        communities.append(list(i))

    element_set = set([paper1, paper2])

    # Check if both elements are in the same list
    for sublist in communities:
        if element_set.issubset(sublist):
            same_comunity = 0
            break
    else:
        same_comunity = 1

    
    return min_edges_removed, communities, same_comunity


