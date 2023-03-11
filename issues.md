Score of minimal_node_remove is wrong.

Keep track of added edges

Check if they are causal, confounded or purely correlational


# Keeping Track of Added Edges

In networkx we can add attributes to edges by doing one of the following:

~~~~python

G.add_edge(1, 2, weight=4.7 )
G.add_edges_from([(3, 4), (4, 5)], color='red')
G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
G[1][2]['weight'] = 4.7
G.edges[3, 4]['weight'] = 4.2

~~~~ 

* Initially we can define all edges to be causal unless otherwise defined.
* Then when we do add removal operations we mark edges added from child's parents are non-causal, and edges added from parent's parent's with the same mark they have (if causal, causal, if both causal and assoicational, both)
* Then we keep doing this. In the final graph, we can keep track of what's causal and what's associational
* Later we need to keep the origin of associational edges as well in terms of which node removals or which abstraction operations introduce them. 


Generally
1. Arcs added from parent's parent are causal
2. Arcs added from children's parent are non-causal
3. If parent's parents are due to previously reversed arcs they are non-causal


---

## Reversing and keeping track of arcs

- You can add due to which node removal operation each node is added. 
- You can reverse an operation by considering the Markov Blanket (MB) of the removed node and removing added edges due to removal, and adding the original edges.
- An interesting question is whether if I remova A and B in this order, can I put A back in without putting B?

The algorithm would be like try to put back MB and remove edges due to removing this node. If all MB is not present, keep the edges of missing places due to MB in. 

Should I think in terms of node arc reversal or node removal?

For this you have to keep track of all assumptions starting from the initial model... E.g. if you there is a causal relation at th ebeginning and if you added causal arcs at each abstraction, you have to keep track of them...

We assume all nodes are unobserved. We also need the abstraction operations for conditioned nodes (which works the opposite,  you want to leave it parentless or with one parent)

BUGS!

Reversal operations

edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
dag = Dag(edges)
abs = Abstraction()
g,order, _, _ = abs.minimal_remove_nodes(dag, [3,5,1], [5])
g.edges()


Output exceeds the size limit. Open the full output data in a text editor
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
File ~/anaconda3/envs/abstraction/lib/python3.11/site-packages/networkx/classes/digraph.py:899, in DiGraph.successors(self, n)
    898 try:
--> 899     return iter(self._succ[n])
    900 except KeyError as err:

KeyError: 1

The above exception was the direct cause of the following exception:

NetworkXError                             Traceback (most recent call last)
Cell In[26], line 4
      2 dag = Dag(edges)
      3 abs = Abstraction()
----> 4 g,order, _, _ = abs.minimal_remove_nodes(dag, [3,5,1], [5])
      5 g.edges()

File ~/Documents/abstraction/abstraction/removal.py:63, in Abstraction.minimal_remove_nodes(self, dag, nodes, observed_nodes)
     61 for node in order:
     62     observed = node in observed_nodes
---> 63     graph, _, score = self.minimal_remove_node(graph, node, observed)
     64 # Scores
     65 num_parents = dict(dag.in_degree()).values()
...
    899     return iter(self._succ[n])
    900 except KeyError as err:
--> 901     raise NetworkXError(f"The node {n} is not in the digraph.") from err

NetworkXError: The node 1 is not in the digraph.

Seems not possible...