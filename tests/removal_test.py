import unittest
from abstraction.dag import Dag
from abstraction.removal import Abstraction

class Test_Abstraction(unittest.TestCase):
    def setUp(self):
        self.abs = Abstraction()
    def test_minimal_remove_node1(self):
        edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
        dag = Dag(edges)
        graph, order, score = self.abs.minimal_remove_node(dag, 4)
        expected = set([(1,3),(2,3),(3,5), (6,5)])
        actual = set(graph.edges)
        self.assertSetEqual(expected, actual)
        self.assertEqual(0, score)
    def test_minimal_remove_node2(self):
        edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
        dag = Dag(edges)
        graph, order, score = self.abs.minimal_remove_node(dag, 3)
        expected = set([(1,4),(2,4),(1,5),(2,5),(4,5),(6,5)])
        actual = set(graph.edges)
        self.assertSetEqual(expected, actual)
        self.assertEqual(4, score)