import sys
#Command line arguments -> Number of nodes, source, sink, glpsol file, output file

class Network:
    _nodes = []
    _nodes_queue1 = []
    _nodes_queue2 = []
    _num_nodes = 0
    _source = 0
    _sink = 0

    _num_paths = 2

    _throughput = 0.0

    _received_count = 0

    def __init__(self, num_nodes, source, sink):
        self._num_nodes = num_nodes + 1
        for i in range(num_nodes+1):
            self._nodes_queue1.append(0)
            self._nodes_queue2.append(0)
            edges = []
            self._nodes.append(edges[:])
        self._source = source
        self._sink = sink

    def add_edge(self, tail, head, etx):
        tup = (head,etx)
        self._nodes[tail].append(tup)

    def print_network(self):
        for i in range(num_nodes):
            for j in range(len(self._nodes[i])):
                print "{0} -> {1} = {2}".format(i, self._nodes[i][j][0], self._nodes[i][j][1])

    def pick_path(self):
        #If the paths do not have same parity, delete the largest one
        #If there is a one hop from source to sink and the cost of the one hop is smaller than
        #the multi hop path -> delete the multi hop and add another single hop
        first_path = self.get_path_length_and_etx(0)
        second_path = self.get_path_length_and_etx(1)
        #print first_path, second_path

        if first_path[0] == 1 :
            if  first_path[1] < second_path[1] :
                self.delete_path(1)
                self.add_edge(self._source, self._sink, first_path[1])
            elif second_path[1] < first_path[1] :
                self.delete_path(0)
                self.add_edge(self._source, self._sink, first_path[1])
            return


        if first_path[0] % 2 != second_path[0] % 2:
            if first_path[1] < second_path[1]:
                self.delete_path(1)
            else:
                self.delete_path(0)
            self._num_paths = 1
            return


    def get_path_length_and_etx(self, path_num): #path_num = 1 or 0
        node = self._source
        path_length = 0
        path_etx = 0

        if len(self._nodes[self._source]) <= 1 and path_num == 1:
            tup = (0,0)
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
        if len(self._nodes[self._source]) <= 1:
            return

        node = self._source
        while node != self._sink:
            if path_num == 1 and node == self._source:
                edge = self._nodes[self._source][1]
                self._nodes[self._source].pop(1)
            else :
                edge = self._nodes[node][0]
                self._nodes[node].pop(0)
            node = edge[0]

    def get_new_transmissions(self, transmission_list):
        new_transmissions = []
        delete_list = []
        for i in range(len(transmission_list)):
            if transmission_list[i][2] <= 0:
                if transmission_list[i][1] != self._sink:
                    new_tail = transmission_list[i][1]
                    new_head = self._nodes[new_tail][0][0]
                    new_etx = self._nodes[new_tail][0][1]
                    transmission = [new_tail, new_head, new_etx]
                    new_transmissions.append(transmission)
                delete_list.append(i)
        for i in range(len(delete_list)):
            del transmission_list[delete_list[i]-i]

        return new_transmissions

    def make_transmissions(self, transmission_list):
        received_at_sink = 0
        
        for i in range(len(transmission_list)):
            transmission_list[i][2] -= 1
            if transmission_list[i][2] <= 0:
                if transmission_list[i][1] == self._sink:
                    received_at_sink += 1

        return received_at_sink

    def is_transmission_happening(self,transmission, transmission_list):
        for i in range(len(transmission_list)):
            if transmission_list[i][0] == transmission[0] and transmission_list[i][1] == transmission[1]:
                return True
        return False

        
    def add_new_transmissions1(self, new_transmissions, transmission_list):
        for i in range(len(new_transmissions)):
            if self.is_transmission_happening(new_transmissions[i], transmission_list):
                self._nodes_queue1[new_transmissions[i][1]] += 1
            else:
                transmission_list.append(new_transmissions[i])

    def add_new_transmissions2(self, new_transmissions, transmission_list):
        for i in range(len(new_transmissions)):
            if self.is_transmission_happening(new_transmissions[i], transmission_list):
                self._nodes_queue2[new_transmissions[i][1]] += 1
            else:
                transmission_list.append(new_transmissions[i])
    
    def send_from_queues1(self, transmission_list):
        for i in range(1, self._num_nodes):
            if self._nodes_queue1[i] > 0:
                tail = i
                if tail == self._sink:
                    continue

                head = self._nodes[tail][0][0]
                etx = self._nodes[tail][0][1]
                transmission = [tail, head, etx]
                if self.is_transmission_happening(transmission, transmission_list):
                    transmission_list.append(transmission)
                    self._nodes_queue1[i] -= 1
    
    def send_from_queues2(self, transmission_list):
        for i in range(1, self._num_nodes):
            if self._nodes_queue2[i] > 0:
                tail = i
                if tail == self._sink:
                    continue
                head = self._nodes[tail][0][0]
                etx = self._nodes[tail][0][1]
                transmission = [tail, head, etx]
                if self.is_transmission_happening(transmission, transmission_list):
                    transmission_list.append(transmission)
                    self._nodes_queue2[i] -= 1
    
    def get_latency(self):
        first_path = self.get_path_length_and_etx(0)
        second_path = self.get_path_length_and_etx(1)
        
        if first_path[1] > second_path[1]:
            return first_path[1]
        return second_path[1]


    def simulate(self, max_time):
        transmission_list0 = []
        transmission_list1 = []
        time = 0
        msgs_received = 0

        while time < max_time:
            if time % 2 == 0:
                #Check which transmissions ended in list 1, and make transmissions (decrement counter) in list 0
                #Send from source to first path
                #Send from the nodes that can send now (have a packet in queue and are from this interval)
                msgs_received += self.make_transmissions(transmission_list0)

                new_transmissions = []
                trans_source = [self._source, self._nodes[self._source][0][0], self._nodes[self._source][0][1]]
                new_transmissions.append(trans_source)
                new_transmissions.extend(self.get_new_transmissions(transmission_list1))

                self.add_new_transmissions1(new_transmissions, transmission_list0)
                self.send_from_queues1(transmission_list0)
                #print "Transmisison list0\n"
                #print transmission_list0
                

            else:
                #Check which transmissions ended in list 0, and make transmissions (decrement counter) in list 1
                #Send from source to second path
                #Send from the nodes that can send now (have a packet in queue and are from this interval)
                msgs_received += self.make_transmissions(transmission_list1)

                new_transmissions = []
                if self._num_paths > 1:
                    trans_source = [self._source, self._nodes[self._source][1][0], self._nodes[self._source][1][1]]
                    new_transmissions.append(trans_source)
                new_transmissions.extend(self.get_new_transmissions(transmission_list0))

                self.add_new_transmissions2(new_transmissions, transmission_list1)
                self.send_from_queues2(transmission_list1)
                #print "Transmisison list1\n"
                #print transmission_list1

            time += 1
        self._throughput = float(msgs_received )/ float(max_time)
        self._received_count = msgs_received










if(len(sys.argv) < 5):
    print "Argumentos insuficientes"
    sys.exit()

num_nodes = int(sys.argv[1])
source = int(sys.argv[2])
sink = int(sys.argv[3])
input_file_name = sys.argv[4]

if input_file_name[7] == 'P':
    output_file_name = "Parity.txt"
else:
    output_file_name = "NoParity.txt"


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

network.pick_path()
#network.print_network()

network.simulate(1000)

#print network._throughput, network._received_count

output_file = open("Throughput" + output_file_name, "a")

output_file.write("{:f}\n".format(network._throughput))

output_file.close()

output_file = open("PathCost" + output_file_name, "a")

output_file.write("{0}\n".format(network.get_latency()))

output_file.close()

"""
network = Network(10,0,5)


for i in range(10):
    for j in range(10):
        network.add_edge(i,j,7)

for i in range(10):
    for j in range(10):
        print network._nodes[i][j]
"""
