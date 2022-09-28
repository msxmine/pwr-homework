import networkx as nx
import subprocess
import random
import math

data = {}
algs = ["dfs", "rw", "rr"]

for n in range(100,2001,100):
    data[n] = {}

    graphs = {}
    starts = {}

    graphs["klika"] = nx.complete_graph(n)
    graphs["path"] = nx.path_graph(n)
    graphs["pathmid"] = nx.path_graph(n)
    treehei = int(math.floor(math.log2(n)))
    graphs["bintree"] = nx.balanced_tree(2, treehei)
    nodes = pow(2, treehei+1)-1
    for nidx in range(n, nodes, 1):
        graphs["bintree"].remove_node(nidx)

    kliksize = math.floor(2*n/3)
    graphs["lolipop"] = nx.lollipop_graph(kliksize, n-kliksize)

    starts["klika"] = random.randrange(0, n)
    starts["path"] = int(math.floor(n/2))
    starts["pathmid"] = 0
    starts["bintree"] = 0
    starts["lolipop"] = random.randrange(0,kliksize)


    for gtype in graphs:
        data[n][gtype] = {}
        indata = ""
        indata += (str(n) + "\n")
        indata += (str(len(graphs[gtype].edges)) + "\n")
        for estar, eend in graphs[gtype].edges:
            indata += (str(estar) + " " + str(eend) + "\n")
        indata += (str(starts[gtype]) + "\n")

        for alg in algs:
            process = subprocess.Popen(["java", "z5", "--alg", alg], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
            result = float(process.communicate(input=indata)[0].strip())
            print(result)
            data[n][gtype][alg] = result

print(data)


