import networkx as nx
import random
import subprocess
import sys

def test():
    indata = ""

    nodes = random.randint(10, 10000)
    startnode = random.randrange(0, nodes)

    graf = nx.gnm_random_graph(nodes, nodes*3)
    graf.add_edges_from(nx.k_edge_augmentation(graf, 1))
    for estar, eend in graf.edges:
        graf[estar][eend]["cost"] = random.uniform(1.0, 10.0)
                        
    indata += (str(nodes) + "\n")
    indata += (str(len(graf.edges)*2) + "\n")
    for estar, eend in graf.edges:
        indata += (str(estar) + " " + str(eend) + " " + str(graf[estar][eend]["cost"]) + "\n")
        indata += (str(eend) + " " + str(estar) + " " + str(graf[estar][eend]["cost"]) + "\n")
    indata += (str(startnode) + "\n")
        
    djikstra = nx.single_source_dijkstra_path_length(graf, startnode, weight="cost")

    process = subprocess.Popen(["java", "z2"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
    stdoutdata, stderrdata = process.communicate(input=indata)

    returned = [ float(x) for x in stdoutdata.split()[1::2]]
    correct = [ djikstra[nidx] for nidx in range(nodes)]

    for idx in range(len(returned)):
        if returned[idx] != correct[idx]:
            print("fail")
            sys.exit(1)
    print("success")

for n in range(1000):
    test()
