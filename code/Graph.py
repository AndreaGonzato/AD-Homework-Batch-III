from copy import deepcopy
from typing import List

from Node import Node


class Graph:
    """
    A graph class that store all the nodes belonging to it

    All the node in a graph need to have unique names.
    """

    def __init__(self, nodes: List[Node]):
        name_list = [node.get_name() for node in nodes]
        flag = len(set(name_list)) == len(nodes)
        if flag:
            self._nodes = nodes
        else:
            raise ValueError('All the node in a graph need to have unique names')

    def __len__(self):
        return len(self._nodes)

    def __repr__(self):
        output = "Graph{\n"
        for node in self._nodes:
            if len(node.get_edges()) > 0:
                for edge in node.get_edges():
                    output += "(" + str(node.get_name()) + " -> " + str(edge.get_cost()) + " -> " + str(edge.get_destination()) + "), "
                output = output[:len(output) - 2]
                output += '\n'
            else:
                output += "(" + str(node.get_name()) + ")\n"
        output += "}"
        return output

    def get_nodes(self) -> List[Node]:
        return self._nodes

    def get_node(self, name: str) -> Node:
        for node in self._nodes:
            if node.get_name() == name:
                return node
        return None

    """
    Return the reversed graph
    
    A reversed graph have all the nodes of the original graph 
    but all the destinations and sources of the edges are swapped
    """
    def get_reversed_graph(self) -> 'Graph':
        reversed_nodes_dictionary = {}

        # declare all the reversed nodes
        for node in self._nodes:
            reversed_nodes_dictionary[node.get_name()] = Node(node.get_name())

        for node in self._nodes:
            for edge in node.get_edges():
                destination = edge.get_destination()
                cost = edge.get_cost()
                reversed_nodes_dictionary.get(destination.get_name()).add_edge(node, cost)

        list_of_reversed_nodes = []
        for v in reversed_nodes_dictionary.values():
            list_of_reversed_nodes.append(v)

        return Graph(list_of_reversed_nodes)

    """
    Return the less important node in the graph.
    
    The node that is returned is the one from which exit less edges.
    In case multiple nodes have the same number of exit edges then the method return one of those.
    """
    def find_a_not_important_node(self) -> Node:
        # find the node with less edges
        global node_to_delete
        min_edges = float('inf')
        for node in self._nodes:
            if min(len(node.get_edges()), min_edges) == len(node.get_edges()):
                min_edges = min(len(node.get_edges()), min_edges)
                node_to_delete = node
        return node_to_delete

    """  
    Return a graph that is similar but it has one less node and all shortcuts that the removed node has.
    
    The node that is deleted can be specified otherwise 
    the method find_a_not_important_node will select one node to be removed.
    """
    def remove_one_node_and_add_his_shortcuts(self, node_to_remove: Node = None) -> 'Graph':
        if len(self._nodes) <= 1:
            raise RuntimeError("The graph has only one node, no shortcut to add")
        new_graph = deepcopy(self)
        if node_to_remove is None:
            node_to_remove = new_graph.find_a_not_important_node()

        for node in new_graph._nodes:
            for i in range(0, len(node.get_edges())):
                # for all the destination of a node

                if node.get_edges()[i].get_destination() == node_to_remove:
                    # add shortcuts
                    first_edge = node.get_edges()[i].get_cost()

                    for j in range(0, len(node_to_remove.get_edges())):
                        destination = node_to_remove.get_edges()[j].get_destination()
                        if destination != node:
                            cost = first_edge + node_to_remove.get_edges()[j].get_cost()
                            node.add_shortcut(destination, cost)

            # remove the edge (node -> node_to_remove)
            node.remove_edge(node_to_remove)

        new_graph._nodes.remove(node_to_remove)
        return new_graph

    """
    return the contraction hierarchies of the graph.
    
    A contraction hierarchies is a sequence of graphs. 
    The next graph in the sequence has always one less node 
    but all the associated shortcuts of the removed node are still present.
    Apart from one node all the other nodes in adjacent graphs in the sequence are the same but may change some edges.
    """
    def get_contraction_hierarchies(self) -> List['Graph']:
        graphs = []
        graph = self
        graphs.append(graph)
        for i in range(len(self._nodes) - 1):
            graph = graph.remove_one_node_and_add_his_shortcuts()
            graphs.append(graph)
        return graphs

    """
    Return a graph with all the shortcuts that are present in all the graphs of the contraction hierarchies
    """
    def add_shortcuts(self) -> 'Graph':
        new_graph = deepcopy(self)
        contraction_graphs = new_graph.get_contraction_hierarchies()

        for node in new_graph._nodes:
            for graph in contraction_graphs:
                contraction_node = graph.get_node(node.get_name())
                if contraction_node is None:
                    continue
                for contraction_edge in contraction_node.get_edges():
                    destination = contraction_edge.get_destination()
                    cost = contraction_edge.get_cost()
                    add_edge = True
                    for edge in node.get_edges():
                        if edge.get_destination() == destination and edge.get_cost() < cost:
                            add_edge = False
                    if add_edge:
                        node.remove_edge(destination)
                        node.add_edge(destination, cost)
        return new_graph






if __name__ == '__main__':
    # declare all the nodes
    nA = Node("A")
    nB = Node("B")
    nC = Node("C")
    nD = Node("D")
    nE = Node("E")
    nF = Node("F")

    # assign the edges
    nA.add_edge(nB, 1)

    nB.add_edge(nC, 1)

    nC.add_edge(nD, 2)

    nD.add_edge(nE, 8)



    # create a graph
    g1 = Graph([nA, nB, nC, nD, nE, nF])
    print("g1", g1)
    g2 = deepcopy(g1)

    print("g2", g2)

    g1.remove_one_node_and_add_his_shortcuts()
    print("g1", g1)
    print("g2", g2)