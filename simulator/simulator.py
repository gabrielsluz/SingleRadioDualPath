import sys
#Command line arguments -> Number of nodes, source, sink, glpsol output file

class Network:
    _nodes = []
    _num_nodes = 0
    _source = 0
    _sink = 0

    _num_paths = 0

    _latency = 0
    _throughput = 0.0

    def __init__(self, num_nodes, source, sink):
        _num_nodes = num_nodes
        for i in range(num_nodes):
            edges = []
            self._nodes.append(edges[:])
        _source = source
        _sink = sink

    def add_edge(self, tail, head, etx):
        tup = (head,etx)
        self._nodes[tail].append(tup)

    def print_network(self):
        for i in range(num_nodes):
            for j in range(len(self._nodes[i])):
                print "{0} -> {1} = {2}".format(i, self._nodes[i][j][0], self._nodes[i][j][1])

    def pick_path(self):
        #If the paths do not have same parity, delete the largest one
        #If there is a one hop from source to sink and the cost of the one hop is smaller than the multi hop path -> delete the multi hop and add another single hop
        first_path = self.get_path_length_and_etx(0)
        second_path = self.get_path_length_and_etx(1)

        if first_path[0] % 2 != second_path[0] % 2:
            if first_path[1] < second_path[1]:
                self.delete_path(1)
            else:
                self.delete_path(0)
            _num_paths = 1
            return

        if first_path[0] == 1 and  first_path[1] < second_path[1] :
            self.delete_path(1)
            self.add_edge(_source, _sink, first_path[1])
        elif second_path[0] == 1 and  second_path[1] < first_path[1] :
            self.delete_path(0)
            self.add_edge(_source, _sink, first_path[1])


    def get_path_length_and_etx(self, path_num): #path_num = 1 or 0
        node = self._source
        path_length = 0
        path_etx = 0

        if len(self._nodes[self._source]) <= 1 and path_num == 1:
            tup = (0,0.0)
            return tup

        while node != self._sink:
            if path_num == 1 and node == self._source:
                edge = self._nodes[self._source][1]
            else :
                edge = self._nodes[node][0]
            node = edge[0]
            path_length += 1
            path_etx += edge[1]

        tup = (path_length, path_etx)
        return tup

    def delete_path(self, path_num):
        if len(self._nodes[self._source]) <= 1
            return

        node = self._source
        while node != self._sink:
            if path_num == 1 and node == self._source:
                edge = self._nodes[self._source][1]
                self._nodes[self._source]pop(1)
            else :
                edge = self._nodes[node][0]
                self._nodes[node].pop(0)
            node = edge[0]

    def send_from_source(self, transmission_list, last_path):




    def simulate(self):
        transmission_list0 = []
        transmission_list1 = []
        time = 0
        msgs_received = 0

        while True:
            if time % 2 == 0:
                #Check which transmissions ended in list 1, and make transmissions (decrement counter) in list 0
                #Send from source to first path
                








if(len(sys.argv) < 5):
    print "Argumentos insuficientes"
    sys.exit()

num_nodes = int(sys.argv[1])
source = int(sys.argv[2])
sink = int(sys.argv[3])
input_file_name = sys.argv[4]

network = Network(num_nodes, source, sink)

input_file = open(input_file_name, "r")

for line in input_file:
    linha = line.split()
    if len(linha) > 1 and linha[1][0] == 'S':
        node_ids = ((linha[1].split('['))[1].split(']'))[0].split(',')
        etx = int(linha[2])
        if etx != 0:
            network.add_edge(int(node_ids[0]), int(node_ids[1]), etx)


input_file.close()

network.print_network()

"""
network = Network(10,0,5)


for i in range(10):
    for j in range(10):
        network.add_edge(i,j,7)

for i in range(10):
    for j in range(10):
        print network._nodes[i][j]
"""
