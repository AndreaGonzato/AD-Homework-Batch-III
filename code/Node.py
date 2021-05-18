from typing import Union, List


class Node(object):
    """
    A node class that represent a node in a weighted graph.

    Each node have a:
        - name: an identifier
        - edges: a list of connection that stars from this node and arrive to another node
    """

    def __init__(self, name: str):
        self._name = name
        self._edges = list()

    def get_name(self) -> str:
        return self._name

    def get_edges(self) -> List['Edge']:
        return self._edges

    def add_edge(self, destination_node: 'Node', cost: Union[int, float]):
        self._edges.append(Edge(destination_node, cost))

    def __eq__(self, o: object) -> bool:
        return self._name.__eq__(o.get_name())

    def __hash__(self) -> int:
        return self._name.__hash__()

    """
    Check if it is really necessary to add a shortcut.
    In case the node has already a equivalent cheaper edge do not add this false shortcut.
    """

    def add_shortcut(self, destination_node: 'Node', cost: Union[int, float]):
        need_to_add_shortcut = True
        for edge in self._edges:
            if edge.get_destination() == destination_node and edge.get_cost() <= cost:
                # I discover a path that is longer than one that I previously have.
                # So I do not need to add this false shortcut
                need_to_add_shortcut = False
            if edge.get_destination() == destination_node and edge.get_cost() > cost:
                # need to update the cost, a better way has just been discover
                need_to_add_shortcut = False
                edge.set_cost(cost)
        if need_to_add_shortcut:
            self.add_edge(destination_node, cost)

    def remove_edge(self, destination_node: 'Node'):
        for edge in self._edges:
            if edge.get_destination() == destination_node:
                self._edges.remove(edge)
                break

    def __repr__(self):
        return self.get_name()


class Edge:
    """
    A class that represent an edge between two nodes in a weighted graph.

    The cost to cross an edge can not be negative.
    Each edge have a:
        - destination: a node that the edge arrive
        - cost: the cost to cross that edge
    """

    def __init__(self, destination: Node, cost: Union[int, float]):
        if cost < 0:
            raise ValueError("a cost to cross an edge can not be negative")
        self._destination = destination
        self._cost = cost

    def __repr__(self):
        return "Edge={destination: " + self._destination.get_name() + \
               ", cost: " + str(self._cost) + " }"

    def get_destination(self) -> Node:
        return self._destination

    def get_cost(self) -> Union[int, float]:
        return self._cost

    def set_cost(self, new_cost: Union[int, float]):
        self._cost = new_cost
