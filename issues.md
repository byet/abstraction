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