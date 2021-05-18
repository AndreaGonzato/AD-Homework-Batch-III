from numbers import Number
from typing import List, Union

from BinaryMinHeap import BinaryMinHeap
from Node import Node

"""
definition of the order criteria

We define a Dijkstra triplet: (node, distance, predecessor).

:parameter
a: (str, Number, str)
    a Dijkstra triplet to compare
b: (str, Number, str)
    a Dijkstra triplet to compare
    
:return
    the result of the comparison    
"""


def has_the_first_triplet_a_lower_distance(a: (str, Number, str), b: (str, Number, str)) -> bool:
    return a[1] <= b[1]


class DijkstraBinaryMinHeap(BinaryMinHeap):
    """
    This class is used to represent a structure that store node distance and predecessor information.
    For each node it store a distance and a predecessor.

    Internally this data are stored in a min heap where in the root there is the node with a minimal distance.
    We define a Dijkstra triplet: (node, distance, predecessor). The node value is the Primary Key of the triplet.
    """

    """
    Build a BinaryMinHeap that store node distance and predecessor information.
    
    :parameter
    nodes: List[Node]
        the list of nodes that the structure will store distance information
    distances: List[Union[int, float]]
        the associated distances of the nodes
    predecessors: List[Node]
        the associates predecessors of the nodes
    
    :raise
        a ValueError when the three lists (nodes, distances, predecessors) have different size
    """

    def __init__(self, nodes: List[Node], distances: List[Union[int, float]], predecessors: List[Node]):
        super().__init__([list(x) for x in zip(nodes, distances, predecessors)],
                         total_order=has_the_first_triplet_a_lower_distance)
        if len(nodes) != len(distances) and len(nodes) != len(predecessors):
            raise ValueError('nodes, distances and predecessors lists of a DijkstraBinaryMinHeap'
                             ' need have the same size')

    """
    Find the Dijkstra triplet in the heap and return its index. In case there is no match then return None    
    
    :parameter
    node: Node
        the node for which it search the index in the min heap
    
    :return
        a number that is the index of the node in the min heap. If there is no match then return None
    """

    def __find_index(self, node: Node) -> Union[int, None]:
        for i in range(0, len(self._A)):
            if self._A[i][0] == node:
                return i
        return None

    """
    Decrease the distance of a Dijkstra triplet that is identify by the node
    
    :parameter
    node: Node 
        the node that identify the Dijkstra triplet
    
    new_distance: Union[int, float]
        the new distance associated to the triplet after the execution
    
    :raise
        a RuntimeError when you try to increase the distance of a Dijkstra triplet
        a RuntimeError when you pass as a parameter a node that is not stored (in the min heap)
    """

    def decrease_distance(self, node: Node, new_distance: Union[int, float]) -> None:
        index = self.__find_index(node)
        if index is None:
            raise RuntimeError("the node do not identify any Dijkstra triplet")
        else:
            if self._A[index][1] < new_distance:
                raise RuntimeError(
                    "distance " + f'{new_distance} is not smaller than ' + f'{self._A[index][1]}' + " in " + f'{self._A[index]}')

            self._A[index][1] = new_distance
            parent = BinaryMinHeap.parent(index)
            while (index != 0 and self._torder(self._A[index], self._A[parent])):
                self._swap_keys(index, parent)
                index = parent
                parent = BinaryMinHeap.parent(index)

    """
    Return the distance of a node
    
    :parameter
    node: Node
        The node that we want to get the distance
    
    :raise
        a RuntimeError when you pass as a parameter a node that is not stored (in the min heap)
    """

    def get_distance_of_a_node(self, node: Node):
        index = self.__find_index(node)
        if index is None:
            raise RuntimeError("the node do not identify any Dijkstra triplet")
        else:
            return self._A[index][1]

    """
    set the predecessor of a node
    
    :parameter
    node: Node
        The node that we are setting the predecessor
    predecessor: Node
        The predecessor that we want to assign to the node
    
    :raise
        a RuntimeError when you pass as a parameter a node that is not stored (in the min heap)    
    """

    def set_predecessor_of_a_node(self, node: Node, predecessor: Node):
        index = self.__find_index(node)
        if index is None:
            raise RuntimeError("the node do not identify any Dijkstra triplet")
        else:
            self._A[index][2] = predecessor
