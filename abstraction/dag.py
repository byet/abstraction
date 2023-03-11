import networkx as nx
from itertools import permutations


class Dag(nx.DiGraph):
    """Extended networkx DAG class that contains abstarction operations."""

    def reversible(self, parent, child):
        """Checks if an arc is reversible without introducing a dag

        Args:
            parent (str): name o parent node
            child (str): name of child node

        Returns:
            bool: True if reversing arc does not introduce a cycle
        """
        return len(list(nx.all_simple_paths(self, parent, child))) == 1

    def reverse_edge(self, parent, child):
        """Reverses an edge in the DAG

        Args:
            parent (str): name o parent node to the edge
            child (str): name of child node to the edge

        Returns:
            (str, str): list of added edges to parent, list of added edges to child in reversal operations
        """
        self.remove_edge(parent, child)
        parent_added_edges = 0
        child_added_edges = 0
        for node in self.predecessors(parent):
            if not self.has_edge(node, child):
                parent_added_edges += 1
                self.add_edge(node, child)
        for node in self.predecessors(child):
            if not self.has_edge(node, parent):
                child_added_edges += 1
                self.add_edge(node, parent)
        self.add_edge(child, parent)
        if not nx.is_directed_acyclic_graph(self):
            Exception(f"Reversing {parent}->{child} leads to a cycle")
        return parent_added_edges, child_added_edges

    def erase_node(self, node, reverse_order=()):
        """Removes node by keeding conditional independencies of the other nodes compatible

        Args:
            node (str): node name to erase
            reverse_order (tuple, optional): order child nodes. If provided, their incoming arcs will be reversed in this order. If not provided, it will use a random reversal order. Defaults to ().

        Returns:
            int: score, i.e. number of added edges during node removal
        """
        children = self.successors(node)
        if reverse_order and set(reverse_order) != set(children):
            ValueError(
                f"Reverse order {set(reverse_order)} is not equivalent to the node children {set(children)}"
            )
        if not reverse_order:
            reverse_order = tuple(children)
        score = 0
        for child in reverse_order:
            if self.reversible(node, child):
                added_edge, _ = self.reverse_edge(node, child)
                score += added_edge
        self.remove_node(node)
        return score

