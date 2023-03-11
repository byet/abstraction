import networkx as nx
from itertools import permutations


class Dag(nx.DiGraph):
    """Extended networkx DAG class that contains abstarction operations."""
    
    def __init__(self, incoming_graph_data=None, all_causal=True, **attr):
        super().__init__(incoming_graph_data, **attr)
        if all_causal:
            for parent, child in self.edges:
                self[parent][child]['causal'] = True
            

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
        edge_attributes = self[parent][child]
        added_edges = []
        num_parent_added_edges = 0
        num_child_added_edges = 0
        # Determine edges to add from parents
        for node in self.predecessors(parent):
            new_edge_attributes = {}
            
            parent_edge_attributes = self[node][parent]
            if parent_edge_attributes.get('causal') and edge_attributes.get('causal'):
               new_edge_attributes['causal'] = True
            if parent_edge_attributes.get('non_causal') or edge_attributes.get('non_causal'):
               new_edge_attributes['non_causal'] = True
            if not self.has_edge(node, child):
                num_parent_added_edges += 1
            added_edges.append((node, child, new_edge_attributes))
        # Determine edges to add from children
        for node in self.predecessors(child):
            if not self.has_edge(node, parent):
                num_child_added_edges += 1
            if node != parent:
                added_edges.append((node, parent, {'non_causal': True}))

        # Update the graph
        self.remove_edge(parent, child)
        self.add_edges_from(added_edges)
        self.add_edge(child, parent, non_causal=True)
        
        if not nx.is_directed_acyclic_graph(self):
            Exception(f"Reversing {parent}->{child} leads to a cycle")
        return num_parent_added_edges, num_child_added_edges

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
            if not self.reversible(node, child):
                raise Exception(f"Arc {node}->{child} cannot be reversed in reverse order {reverse_order}")    
            added_edge, _ = self.reverse_edge(node, child)
            score += added_edge
        self.remove_node(node)
        return score
    
    def erase_observed_node(self, node, reverse_order=()):
        """Removes observed node by keeding conditional independencies of the other nodes compatible
        In order to remove an observed node it should not have any parents.
        When it has one parent, it may open converging paths high above (2 levels above) such as A->C<-B; C->D

        Args:
            node (str): node name to erase
            reverse_order (tuple, optional): order child nodes. If provided, their incoming arcs will be reversed in this order. If not provided, it will use a random reversal order. Defaults to ().

        Returns:
            int: score, i.e. number of added edges during node removal
        """
        parents = self.predecessors(node)
        if reverse_order and set(reverse_order) != set(parents):
            ValueError(
                f"Reverse order {set(reverse_order)} is not equivalent to the node parents {set(parents)}"
            )
        if not reverse_order:
            reverse_order = tuple(parents)
        score = 0
        for parent in reverse_order:
            if not self.reversible(parent, node):
                raise Exception(f"Arc {parent}->{node} cannot be reversed in reverse order {reverse_order}")    
            added_edge, _ = self.reverse_edge(parent, node)
            score += added_edge
        self.remove_node(node)
        return score