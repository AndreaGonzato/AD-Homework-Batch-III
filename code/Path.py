from Node import Node


class Path(object):
    """
    A Path class that describe a path in a weighted graph

    All the path have a:
    - source: a starting node in the graph
    - target: the ending node of the path
    - nodes: a list of nodes in the path. The order in the list imply the node succession in the path
    - edges: a list of edges that are crossed during the path.
    - total cost: the cost to do all the path.
    """

    def __init__(self, source_node: Node):
        self._source = source_node
        self._target = source_node
        self._nodes = [source_node]
        self._edges = []
        self._total_cost = 0

    def add_connection(self, next_node: Node):
        nodes_disconnected = True
        for edge in self._target.get_edges():
            if edge.get_destination() == next_node:
                self._edges.append(edge)
                self._total_cost += edge.get_cost()
                nodes_disconnected = False
                break
        if nodes_disconnected:
            raise RuntimeError(
                f"Can not add {next_node} to the path sine is not connected to {self._nodes[len(self._nodes) - 1]}")
        self._target = next_node
        self._nodes.append(next_node)

    def __repr__(self):
        if len(self._nodes) == 1:
            return "(" + str(self._source.get_name()) + ")" + " total cost: " + str(self._total_cost)

        output = "(" + str(self._nodes[0].get_name())
        for edge in self._edges:
            output += " -> " + str(edge.get_cost()) + " -> " + str(edge.get_destination())
        output += ") total cost: " + str(self._total_cost)
        return output

    def __add__(self, other):
        for node in other._nodes:
            if node is not other._source:
                self.add_connection(node)
        return self
