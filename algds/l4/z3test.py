import networkx as nx
import random
import subprocess
import sys

def test():
    indata = ""

    nodes = random.randint(10, 50000)

    graf = nx.gnm_random_graph(nodes, nodes*3)
    graf.add_edges_from(nx.k_edge_augmentation(graf, 1))
    for estar, eend in graf.edges:
        graf[estar][eend]["cost"] = random.uniform(1.0, 10.0)
                        
    indata += (str(nodes) + "\n")
    indata += (str(len(graf.edges)) + "\n")
    for estar, eend in graf.edges:
        indata += (str(estar) + " " + str(eend) + " " + str(graf[estar][eend]["cost"]) + "\n")
        
    mstedges = nx.minimum_spanning_edges(graf, algorithm="kruskal", weight="cost", data=True)
    mstcorrect = 0.0
    for estart, eend, edata in mstedges:
        mstcorrect += edata["cost"]

    processprim = subprocess.Popen(["java", "z3", "-p"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
    processkrusk = subprocess.Popen(["java", "z3", "-k"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
    
    stdoutdatapr, stderrdatapr = processprim.communicate(input=indata)
    stdoutdatakr, stderrdatakr = processkrusk.communicate(input=indata)
    
    primres = float(stdoutdatapr.split()[-1])
    kruskres = float(stdoutdatakr.split()[-1])
    
    primdiff = abs(mstcorrect - primres)
    kruskdiff = abs(mstcorrect - kruskres)
    
    if (primdiff > 0.000001 or kruskdiff > 0.000001):
        print(primres)
        print(kruskres)
        print(mstcorrect)
        print("fail")
        sys.exit(1)
        
    print("success")

for n in range(100):
    test()
