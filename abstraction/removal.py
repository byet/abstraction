from itertools import permutations
from abstraction.dag import Dag


class Abstraction:
    def __init__(self) -> None:
        pass

    def minimal_remove_node(self, dag, node):
        """Removes a node by introducing minimal number of additional arcs.

        Args:
            dag (Dag): DAG object
            node (str): node name

        Returns:
            Dag, int: returns both the simplified DAG, and score (number of additional edges)
        """
        children = dag.successors(node)
        reverse_orders = permutations(children)
        best_score = float("inf")
        best_order = []
        G = Dag()
        for order in reverse_orders:
            graph = dag.copy()
            score = graph.erase_node(node, reverse_order=order)
            print(score)
            if score < best_score:
                G = graph.copy()
                best_score = score
                best_order = order
        return G, best_order, best_score

    def minimal_remove_nodes(self, dag, nodes):
        """Removes a set of nodes node by introducing minimal number of additional arcs.

        Args:
            dag (Dag): DAG object
            nodes (list): list of node names to be removed.

        Returns:
            Dag, order int, int: Abstracted dag object, list of removed nodes, maximum number of parents in the dag, the total number of parents in the dag
        """
        remove_orders = permutations(nodes)
        best_score1 = float("inf")
        best_score2 = float("inf")
        best_order = []
        G = Dag()
        for order in remove_orders:
            graph = dag.copy()
            for node in order:
                graph, score = self.minimal_remove_node(graph, node)
            # Scores
            num_parents = dict(dag.in_degree()).values()
            score1 = max(num_parents)
            score2 = sum(num_parents)
            if score1 < best_score1:
                G = graph.copy()
                best_score1 = score1
                best_order = order
            elif score2 < best_score2:
                G = graph.copy()
                best_score2 = score2
                best_order = order
        return G, best_order, best_score1, best_score2
