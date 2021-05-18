from typing import List, Tuple, Union, Any

from DijkstraBinaryMinHeap import DijkstraBinaryMinHeap
from Graph import Graph
from Node import Node
from Path import Path

positive_infinity = float('inf')

"""
    Find the min distance from a node source to all the nodes in the graph (G).
    
    :return
        a DijkstraResult
"""
def binary_heap_dijkstra(G: Graph, source: Node) -> 'DijkstraResult':
    distances = [positive_infinity for i in range(0, len(G))]
    predecessors = [None for i in range(0, len(G))]
    dbmh = DijkstraBinaryMinHeap(G.get_nodes(), distances, predecessors)

    # set the node s distance equal to zero
    dbmh.decrease_distance(source, 0)
    result = []
    while len(dbmh) > 0:
        current_triplet = dbmh.remove_root()
        result.append(current_triplet)
        if current_triplet[1] == positive_infinity:
            pass

        for i in range(0, len(current_triplet[0].get_edges())):
            destination = current_triplet[0].get_edges()[i].get_destination()
            new_path_cost = current_triplet[1] + current_triplet[0].get_edges()[i].get_cost()
            if new_path_cost < dbmh.get_distance_of_a_node(destination):
                dbmh.decrease_distance(destination, new_path_cost)
                dbmh.set_predecessor_of_a_node(destination, current_triplet[0])
    return DijkstraResult(result)


def __initialize_search(graph: Graph, distance_dictionary, predecessor_dictionary):
    for node in graph.get_nodes():
        distance_dictionary[node] = positive_infinity
        predecessor_dictionary[node] = None


def __find_nearest_node(distance_dictionary) -> Node:
    min_distance = positive_infinity
    nearest_node = None
    for key in distance_dictionary:
        value = distance_dictionary[key]
        if value < min_distance:
            min_distance = value
            nearest_node = key
        if nearest_node is None:
            nearest_node = key
    return nearest_node


def __explore_node_neighbors(nearest_node: Node, distance_dictionary, predecessor_dictionary, result):
    for edge in nearest_node.get_edges():
        distance_new_visit = distance_dictionary[nearest_node] + edge.get_cost()
        destination = edge.get_destination()
        if destination in distance_dictionary and \
                distance_new_visit < distance_dictionary[destination]:
            # just found a better path
            distance_dictionary[destination] = distance_new_visit
            predecessor_dictionary[destination] = nearest_node

    # store the dijkstra result of the nearest_node
    result.append(
        [nearest_node, distance_dictionary[nearest_node], predecessor_dictionary[nearest_node]])
    # remove the node from the distance_dictionary
    distance_dictionary.pop(nearest_node)


"""
This method compute the shortest path from a source node to a target node in a graph.

Internally it alternate between forward search and backward search in a bidirectional dijkstra search.
It stop when a sufficient amount of middle nodes are fully discovered in both the forward and backward search.
Then for each of those middle nodes it find the min distance from source to target 
as: min{d(source, middle) + d(middle, target)} and return the min path and two DijkstraResult, 
one for the forward search and one for the backward search.

:return
a Tuple[Path, DijkstraResult, DijkstraResult]
Where the first element of the tuple is the shortest path from the source node to the target node
The second element is the result of the forward Dijkstra search
The third element is the result of the backward Dijkstra search
"""
def bidirectional_dijkstra(graph: Graph, source: Node, target: Node) -> Tuple[Path, 'DijkstraResult', 'DijkstraResult']:
    # generate a reversed graph
    reversed_graph = graph.get_reversed_graph()

    distance_forward_dictionary = {}
    distance_backward_dictionary = {}
    predecessor_forward_dictionary = {}
    predecessor_backward_dictionary = {}

    # initialize search
    __initialize_search(graph, distance_forward_dictionary, predecessor_forward_dictionary)
    __initialize_search(reversed_graph, distance_backward_dictionary, predecessor_backward_dictionary)

    distance_forward_dictionary[source] = 0
    distance_backward_dictionary[target] = 0

    forward_result = list()
    backward_result = list()

    count = 0
    while len(distance_forward_dictionary) > 0 and len(distance_backward_dictionary) > 0:
        if count % 2 == 0:
            # -- forward search --

            # find the nearest_node
            nearest_node = __find_nearest_node(distance_forward_dictionary)

            if distance_forward_dictionary[nearest_node] == positive_infinity:
                # if the nearest_node is not connected to the graph
                break

            # explore
            __explore_node_neighbors(nearest_node, distance_forward_dictionary, predecessor_forward_dictionary,
                                     forward_result)

            if nearest_node not in distance_backward_dictionary:
                # stop criteria
                break

        else:
            # -- backward search --

            # find the nearest_node
            nearest_node = __find_nearest_node(distance_backward_dictionary)

            if distance_backward_dictionary[nearest_node] == positive_infinity:
                # if the nearest_node is not connected to the graph
                break

            # explore
            __explore_node_neighbors(nearest_node, distance_backward_dictionary, predecessor_backward_dictionary,
                                     backward_result)

            if nearest_node not in distance_forward_dictionary:
                # stop criteria
                break
        count += 1

    # <- end while

    # continue the forward/backward search up to forward/backward_search_distance_terminator
    forward_search_distance_terminator = forward_result[len(forward_result) - 1][1] + \
                                         backward_result[len(backward_result) - 1][1] - \
                                         backward_result[len(backward_result) - 2][1]
    backward_search_distance_terminator = backward_result[len(backward_result) - 1][1] + \
                                          forward_result[len(forward_result) - 1][1] - \
                                          forward_result[len(forward_result) - 2][1]

    # --- continue forward search ---
    while len(distance_forward_dictionary) > 0:
        # find the nearest_node
        nearest_node = __find_nearest_node(distance_forward_dictionary)

        # if the nearest_node is not connected to the graph
        if distance_forward_dictionary[nearest_node] == positive_infinity:
            break

        # if the nearest_node is too far
        if distance_forward_dictionary[nearest_node] > forward_search_distance_terminator:
            # stop criteria
            break

        # explore
        __explore_node_neighbors(nearest_node, distance_forward_dictionary, predecessor_forward_dictionary,
                                 forward_result)

    # --- continue backward search ---
    while len(distance_backward_dictionary) > 0:
        # find the nearest_node
        nearest_node = __find_nearest_node(distance_backward_dictionary)

        # if the nearest_node is not connected to the graph
        if distance_backward_dictionary[nearest_node] == positive_infinity:
            break

        # if the nearest_node is too far
        if distance_backward_dictionary[nearest_node] > backward_search_distance_terminator:
            # stop criteria
            break

        # explore
        __explore_node_neighbors(nearest_node, distance_backward_dictionary, predecessor_backward_dictionary,
                                 backward_result)

    # end while

    forward_result_dictionary = {}
    backward_result_dictionary = {}

    for element in forward_result:
        forward_result_dictionary[element[0]] = [element[1], element[2]]

    for element in backward_result:
        backward_result_dictionary[element[0]] = [element[1], element[2]]

    # ---- determine the interconnection_node from forward search and backward search  ----
    nodes_fully_explored_in_forward_search_set = set(forward_result_dictionary.keys())
    nodes_fully_explored_in_backward_search_set = set(backward_result_dictionary.keys())

    # determine nodes that are fully explored in both forward search and backward search
    intersection = nodes_fully_explored_in_backward_search_set.intersection(nodes_fully_explored_in_forward_search_set)

    min_cost = positive_infinity
    interconnection_node = None
    for node in intersection:

        forward_cost = forward_result_dictionary[node][0]
        backward_cost = backward_result_dictionary[node][0]

        cost = forward_cost + backward_cost
        if cost < min_cost:
            min_cost = cost
            interconnection_node = graph.get_node(node.get_name())

    # ----- determine the path from source to target -----

    if interconnection_node is None:
        return None, forward_result, backward_result

    # build the backward path
    backward_path = Path(interconnection_node)
    if interconnection_node != target:
        node = interconnection_node
        while True:
            destination_name = backward_result_dictionary[node][1].get_name()
            destination = graph.get_node(destination_name)
            backward_path.add_connection(destination)
            node = destination
            if destination == target:
                break

    # build a queue that put all the nodes in the path from the interconnection_node to the source
    forward_path_queue = [interconnection_node]
    if interconnection_node != source:
        node = interconnection_node
        while True:
            departure_node = forward_result_dictionary[node][1]
            forward_path_queue.append(departure_node)
            node = departure_node
            if departure_node == source:
                break

    # build forward path by extracting the nodes from the queue
    forward_path = Path(forward_path_queue.pop())
    while len(forward_path_queue) > 0:
        forward_path.add_connection(forward_path_queue.pop())

    # join the two paths
    total_path = forward_path + backward_path

    return total_path, DijkstraResult(forward_result), DijkstraResult(backward_result)


class DijkstraResult:
    """
    A class that represent in a proper way the result of a Dijkstra algorithm.

    If the Dijkstra result is correct and how you obtain it is not a matter of this class.
    This class do not implement any logic or control. It just print a List[Tuple] in a nice way.
    It store a List[Tuple] that describe the shortest path for each node.
    The first element in the tuple is a node
    The second element in the tuple is a number that describe the cost to reach that node from the source.
    The third element is the previous node that is in the path from the source to the node before reaching the node.
    """

    def __init__(self, result: List[Tuple[Node, Union[int, float], Node]]):
        self._result = result

    def __repr__(self):
        output = "Node | Distance | Predecessor\n"
        for row in self._result:
            output += str(row[0]).rjust(3) + str(row[1]).rjust(9) + str(row[2]).rjust(12) + "\n"
        return output

if __name__ == '__main__':
    nA = Node("A")
    nB = Node("B")

    # assign the edges
    nA.add_edge(nB, 5)

    graph = Graph([nA, nB])

    a,b,c = bidirectional_dijkstra(graph, nA, nB)
    print(a)
    print(b)
    print(c)

