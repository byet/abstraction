# Abstraction

Abstraction makes causal DAG abstraction operations. It depends on `networkx`.

## Installation

~~~~python
pip install git+https://github.com/byet/abstraction.git
~~~~

## Example

~~~python
from abstraction.dag import Dag
from abstraction.removal import Abstraction

edges = [(1,3),(2,3),(3,4),(3,5), (1,4), (6,5)]
dag = Dag(edges)

abs = Abstraction()

g1, score = abs.minimal_remove_node(dag, 3)

g2, score1, score2 = abs.minimal_remove_nodes(dag, (2,3))
~~~