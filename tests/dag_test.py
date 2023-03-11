import unittest
from abstraction.dag import Dag

class Test_Dag(unittest.TestCase):
    def test_reversible(self):
        edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
        dag = Dag(edges)
        self.assertTrue(dag.reversible(1,3))
        self.assertFalse(dag.reversible(1,4))



    def test_reverse_edge(self):
        edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
        dag = Dag(edges)
        dag.reverse_edge(1,3)
        expected = set([(3,1),(2,3),(3,4),(3,5), (1,4), (6,5), (2,1)])
        actual = set(dag.edges)
        self.assertSetEqual(expected, actual)

    def test_erase_node1(self):
        edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
        dag = Dag(edges)
        dag.erase_node(6)
        expected = set([(1,3),(2,3),(3,4),(3,5), (1,4)])
        actual = set(dag.edges)
        self.assertSetEqual(expected, actual)

    def test_erase_node2(self):
        edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
        dag = Dag(edges)
        dag.erase_node(3, reverse_order=(4,5))
        expected = set([(1,4), (6,5), (2,4), (2,5), (4,5), (1,5)])
        actual = set(dag.edges)
        self.assertSetEqual(expected, actual)

  