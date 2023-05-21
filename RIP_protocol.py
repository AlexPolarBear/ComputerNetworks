import random
import socket
import struct

class network:

    def __init__(self):
        self.nodes = {}
    
    def add_node(self, ip, key):
        if ip not in self.nodes:
            self.nodes[key] = node(ip, self, key)
        else:
            pass
        
    def add_edge(self, key_a, key_b, ip_a, ip_b):
        self.nodes[key_a].add_neighbor(key_b, ip_b)
        self.nodes[key_b].add_neighbor(key_a, ip_a)

    def update(self):
        upd = 0
        for key in self.nodes:
            upd += self.nodes[key].update()
        return upd != 0

    def gets(self, key):
        if key in self.nodes:
            return self.nodes[key]
        else:
            return None


class node:

    def __init__(self, ip, net, key):
        self.ip = ip
        self.net = net
        self.ip_table = {key: (0, ip)}

    def add_neighbor(self, key, ip):
        self.ip_table[key] = (1, ip)
        
    def updating(self, key):
        upd = False
        node = self.net.gets(key)
        for k, v in node.ip_table.items():
            if k not in self.ip_table:
                self.ip_table[k] = (v[0]+1, node.ip)
                upd = True
            else:
                if self.ip_table[k][0] > v[0]+1:
                    self.ip_table[k] = (v[0]+1, node.ip)
                    upd = True
        return upd

    def update(self):
        neighbors = [key for key, val in self.ip_table.items() if val[0] == 1]
        upd = 0
        for key in neighbors: 
            upd += self.updating(key)
        return upd != 0


if __name__ == "__main__":
    net = network()
    for key in range(1, 4):
        ip_a = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        ip_b = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        net.add_node(ip_a, key)
        net.add_node(ip_b, key+1)
        net.add_edge(key, key+1, ip_a, ip_b)

    max_iter = 4
    ips =  []
    while max_iter > 0 and net.update():
        val = (net.gets(max_iter-1).ip_table).values()
        for v in val:
            if v[1] not in ips:
                ips.append(v[1])
                print(f"\nFinal state of router {v[1]} table:")
                print("[Source IP]\t\t[Destination IP]\t[Next Hop]\t[Metric]")
                
                i = 0
                next_hop = 0
                while i != len(val):
                    if v == list(val)[i]:
                        if list(val)[i][0] == 0 or len(val) > 2:
                            next_hop = list(val)[i+1][1]
                        else:
                            next_hop = list(val)[i-1][1]
                    i += 1                    
                
                for key in net.nodes:
                    new = net.gets(key).ip_table
                    dest = new.get(key)[1]
                    if dest == v[1] and key < 4:
                        new = net.gets(1).ip_table
                        dest = new.get(key-1)[1]
                    if dest == v[1] and key == 4:
                        new = net.gets(1).ip_table
                        dest = new.get(key-1)[1]
                    for k, vl in new.items():
                        if vl[1] == dest:
                            metric = k
                            if dest == next_hop:
                                metric = 1
                    print(f"{v[1]}\t\t{dest}\t\t{next_hop}\t  {metric}")
            else:
                continue
        max_iter -= 1
