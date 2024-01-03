import random
import networkx as nx

def find_components_dfs(graph):
    visited = set()
    components = []

    def dfs(node, component):
        '''
        The inner function dfs performs a recursive depth-first search starting from a given node. It adds the current node to the visited set and the current connected component. Then, for each neighbor of the current node, if the neighbor has not been visited, it recursively calls the dfs function on that neighbor.
        '''
        # Adding the node to the visited
        visited.add(node)
        # Adding the node to the set of component new_component called
        component.add(node)

        for neighbor in graph[node]:
            # Recursively calling dfs on the neighbours
            if neighbor not in visited:
                dfs(neighbor, component)

    #for each unvisited node in the graph
    for node in graph:
        if node not in visited:
            # we create a component - each node can be pontentially a component.
            #We're initialiating the component
            new_component = set()
            # Adding the neighbour node to the visited nodes
            dfs(node, new_component)
            # and to the components initial list
            components.append(new_component)

    # The function returns a list of connected components.
    return components


def contract_edge(graphr, u, v):
    '''
    Performs a contraction : given two nodes and a graph it return a new graph
    were the two nodes were joint and the edges appropriatly contracted
    '''
    # We create an edge we call in a name such that I can recognise the nodes from which the edge was conctracted
    contracted_node = f"{u}_{v}"

    # Add the new node to the graph
    graphr.add_node(contracted_node)

    # Dictionaries of nodes and his neighbours
    nn = graphr.adj[v].items()
    # Add the edges to new node which before were connected to u
    for neighbor, edge_data in nn:
        if neighbor != v:
            # using ** to copy all attributes of the edges (weights or examples)
            graphr.add_edge(contracted_node, neighbor, **edge_data)

    # Add the edges to new node which before were connected to v
    for neighbor, edge_data in nn:
        if neighbor != u:
            graphr.add_edge(contracted_node, neighbor, **edge_data)

    # Remove u and v from the graph
    graphr.remove_node(u)
    graphr.remove_node(v)

    return graphr



def custom_karger(graph, node1, node2):
    '''
    This function is a variation of the karger algorithm. Given two nodes it returns the edges we
    need to cut so that minimizes the number of edges to be cut. It this edges are removed we should get
    two connected component such that the first and second node beolngs to the first and second component
    rispectivly. Does NOT return a optimal solution as selects the edges randomly. This approch performs
    on average quite good and efficienty but sometimes may fail or return a non-optimal solution.
    '''
    # We create a copy of the original graph
    graph_original=graph.copy()
    # And one more to perform the contraction
    gr = graph.copy()
    # We keep contracting while
    while len(gr.nodes()) > 2 and len(gr.edges()) > 0:
        # Select casually edges to contract
        edge = random.choice(list(gr.edges()))
        # Identify the nodes incident on the edge
        u, v = edge

        # Contract the selected edge
        graph = contract_edge(gr, u, v)

    # Returns the connected components
    components = list(find_components_dfs(gr))

    #creare a list for all connected components
    first_elements = [[] for _ in range(len(components))]
    # a counter to go through the list
    i=0
    # To store the mincut
    res= []

    # Apply conversion
    for elem in components:
        # first from set component I convert it to a ist
        elements_list = list(elem)

        # I extract all element from the, now, list
        # Get all the original nodes from the list of contracted node, if a list
        for element in elements_list:
            if type(element)!=int:
                node = element.split('_')
                node = [int(elem) for elem in node]
                try:
                    first_elements[i]+=node
                except IndexError:
                     return ("Retry")
            # If a component is a number because made up of a node only
            else:
                # append the elemnt to the list
                first_elements[i].append(element)
            i +=1

    # Select only the component with the two node of interest
    f_elements = [elem for elem in first_elements if node1 in elem or node2 in elem]

    # Initialize local variabile to store the minicut
    #nmin = 0
    # Andd the total weight of the mincut
    #totw=0
    if len(f_elements)==2:
        for u in f_elements[0]:
            for v in f_elements[1]:
                # Check if edge which connect the contracted nodes exists
                if graph_original.has_edge(str(u),str(v)) or graph_original.has_edge(str(v),str(u)):
                #    nmin += 1
                    # get informations about the edges
                    #edge_data = graph.get_edge_data(u, v)
                    #print('edge', edge_data)
                    # Extract the weight if we want to take it into account
                    #peso_arco = edge_data['weight']
                    # adding the weight to store the total cost of that cut
                    #totw += peso_arco
                    # And add it to the result
                    res.append((u,v))
        # Eventually return the length of the shortest path directly
        #res.append(nmin)
        # Evenetually modify res so to store the total weight of the cut
        #res.append(totw)
        return(res)

    # When something went wrong in the contraction
    else:
        return "Retry, maybe iteration is key"



def considerweight(GG,n1,n2, it=10):
    res1=[[]]
    j=0
    while j<it:
        # Iterates to get multiple cuts for sake of consistency
        a= custom_karger(GG,n1, n2)
        res1[0].append(a)
        j+=1
    return(res1)

def weigthedmincut(listres1):
    # Retrieves only the lists
    edges_with_weights = [item[0] for item in listres1 if isinstance(item, list) and len(item) == 2 and item!="Retry"]

    # Get the edges with minimum weigth
    min_weight_edge = min(edges_with_weights, key=lambda x: x[1])

    return(min_weight_edge)

