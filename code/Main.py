from Dijkstra import binary_heap_dijkstra, bidirectional_dijkstra
from Graph import Graph
from Node import Node


def get_a_graph() -> Graph:
    # declare all the nodes
    nA = Node("A")
    nB = Node("B")
    nC = Node("C")
    nD = Node("D")
    nE = Node("E")
    nF = Node("F")

    # assign the edges
    nA.add_edge(nD, 1)
    nA.add_edge(nB, 5)

    nB.add_edge(nC, 1)
    nB.add_edge(nE, 4.5)

    nC.add_edge(nE, 2)
    nC.add_edge(nA, 4)

    nD.add_edge(nB, 2.2)
    nD.add_edge(nF, 10)
    nD.add_edge(nE, 8)

    nE.add_edge(nF, 1)
    nE.add_edge(nC, 3)

    nF.add_edge(nB, 3)
    nF.add_edge(nD, 6)
    nF.add_edge(nC, 5)

    # create a graph
    return Graph([nA, nB, nC, nD, nE, nF])


if __name__ == '__main__':
    # '''
    print("EXERCISE 1")

    # create a graph
    G = get_a_graph()

    # get a node of the graph, this will be the source in Dijkstra
    source_node = G.get_nodes()[0]

    # call dijkstra
    dijkstra_result = binary_heap_dijkstra(G, source_node)

    # show result
    print(dijkstra_result)

    # '''

    # '''
    print("\n\nEXERCISE 2A")
    # create a graph
    G = get_a_graph()

    print("initial G =", G)

    graph_with_shortcuts = G.add_shortcuts()
    print("\ngraph_with_shortcuts:", graph_with_shortcuts)

    print("\nall the contraction hierarchies of the graph are:")
    count = 0
    contraction_hierarchies = G.get_contraction_hierarchies()
    for graph in contraction_hierarchies:
        print(f"level: {count}", graph, "\n")
        count += 1

    # '''

    # '''
    print("\n\nEXERCISE 2B")
    # create a graph
    G = get_a_graph()
    graph_with_shortcuts = G.add_shortcuts()
    source = graph_with_shortcuts.get_nodes()[0]
    target = graph_with_shortcuts.get_nodes()[len(graph_with_shortcuts.get_nodes()) - 1]
    print(
        f"now we call bidirectional_dijkstra on the graph_with_shortcuts with source node {source} and target node {target}")

    path, forward_dijkstra, backward_dijkstra = bidirectional_dijkstra(graph_with_shortcuts, source, target)

    # show result
    print("shortest path:", path)
    print("\nforward dijkstra result\n", forward_dijkstra)
    print("\nbackward dijkstra result\n", backward_dijkstra)
    # '''


