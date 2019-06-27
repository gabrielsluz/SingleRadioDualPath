from copy import deepcopy

class Network:
    nodes = []
    _num_nodes = 0

    def __init__(self, num_nodes):
        _num_nodes = num_nodes
        for i in range(num_nodes):
            edges = []
            self.nodes.append(edges[:])

    def add_edge(self, tail, head, etx):
        tup = (head,etx)
        self.nodes[tail].append(tup)


network = Network(10)

for i in range(10):
    for j in range(10):
        network.add_edge(i,j,7)

for i in range(10):
    for j in range(10):
        print network.nodes[i][j]
