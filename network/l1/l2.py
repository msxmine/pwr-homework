import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

random.seed(1)

m = 100


def gennet():
    siec = nx.Graph()
    siec.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (0, 6), (5, 7), (6, 7), (6, 8), (2, 8), (2, 9), (8, 9), (8, 10), (9, 10), (10, 13), (3, 11), (11, 13), (3, 12), (12, 14), (4, 15), (15, 17), (14, 17), (4, 16), (16, 18), (18, 19), (1, 19)])
    for ea, eb in siec.edges:
        siec[ea][eb]["capacity"] = 0
        siec[ea][eb]["actual"] = 0
    return siec

def genlmat(nodesnum=20):
    N = np.zeros((nodesnum,nodesnum))
    for start in range(nodesnum):
        for end in range(nodesnum):
            if start != end:
                N[start][end] = random.randint(20, 100)
    return N

def calcload(graf, lmat):
    for start in range(len(graf.nodes)):
        for end in range(len(graf.nodes)):
            if start !=  end:
                path = nx.shortest_path(graf, source=start, target=end)
                for sn, en in zip(path, path[1:]):
                    graf[sn][en]["actual"] += lmat[start][end]

def upgradecapacity(graf):
    for ea, eb in graf.edges:
        graf[ea][eb]["capacity"] = random.uniform(1.5, 3.5) * graf[ea][eb]["actual"] * m
    
def avglat(graf, lmat):
    nodesnum = len(graf.nodes)
    G = 0
    for start in range(nodesnum):
        for end in range(nodesnum):
            G += lmat[start][end]
    Se = 0
    for ea, eb in graf.edges:
        ae = graf[ea][eb]["actual"]
        ce = graf[ea][eb]["capacity"]
        Se += ( ae / (ce/m - ae) )
    return (1/G) * Se

            
def reliabilitytest(grafmr, lmat, dmgprob, tmax, maxeload=1.0):
    graf = grafmr.copy()
    for ea, eb in graf.edges:
        if random.uniform(0, 1) < dmgprob:
            graf.remove_edge(ea, eb)
        else:
            graf[ea][eb]["actual"] = 0
    if not nx.is_connected(graf):
        return False
    for start in range(len(graf.nodes)):
        for end in range(len(graf.nodes)):
            if start != end:
                tgraf = graf.copy()
                for es, ee in tgraf.edges:
                    if (tgraf[es][ee]["actual"] + lmat[start][end]) * m > maxeload * tgraf[es][ee]["capacity"]:
                        tgraf.remove_edge(es, ee)
                try:
                    path = nx.shortest_path(tgraf, source=start, target=end)
                except nx.NetworkXNoPath:
                    return False
                for sn, en in zip(path, path[1:]):
                    graf[sn][en]["actual"] += lmat[start][end]
    T = avglat(graf, lmat)
    #print(T)
    return T < tmax


def reliabilitystat(graf, lmat, dmgprob, tmax, tests=1000, maxeload=1.0):
    successes = 0
    for testidx in range(tests):
        if reliabilitytest(graf, lmat, dmgprob, tmax, maxeload):
            successes += 1
    return successes/tests


def showgraph():
    siec = gennet()
    nx.draw(siec)
    plt.show()

def zada():
    Grafsiec = gennet()
    macNat = genlmat(len(Grafsiec.nodes))
    calcload(Grafsiec, macNat)
    upgradecapacity(Grafsiec)
    wyniki = []
    extraload = []
    for iterv in range(30):
        extraload.append(iterv*2)
        N = macNat.copy()
        for col in range(N.shape[0]):
            for row in range(N.shape[1]):
                N[col][row] += iterv*2
        wyniki.append(reliabilitystat(Grafsiec, N, 0.05, 0.02, tests=1000))
    plt.plot(extraload, wyniki)
    plt.show()
    print(wyniki)
    print(extraload)
        

def zadb():
    Grafsiec = gennet()
    macNat = genlmat(len(Grafsiec.nodes))
    calcload(Grafsiec, macNat)
    upgradecapacity(Grafsiec)
    wyniki = []
    extracapacity = []
    for iterv in range(60):
        extracapacity.append(iterv*150)
        siec = Grafsiec.copy()
        for est, eed in siec.edges:
            siec[est][eed]["capacity"] += iterv*150*m
        wyniki.append(reliabilitystat(siec, macNat, 0.05, 0.02, tests=200, maxeload=0.9))
    plt.plot(extracapacity, wyniki)
    plt.axis([0, 60*150, 0, 1])
    plt.show()
    print(wyniki)
    print(extracapacity)
    

def zadc():
    Grafsiec = gennet()
    macNat = genlmat(len(Grafsiec.nodes))
    calcload(Grafsiec, macNat)
    upgradecapacity(Grafsiec)
    wyniki = []
    extraedgesnum = []
    extraeset = list(nx.non_edges(Grafsiec))
    extraemax = len(extraeset)
    avgcap = 0
    for est, eed in Grafsiec.edges:
        avgcap += Grafsiec[est][eed]["capacity"]
    avgcap /= len(Grafsiec.edges)
    print(extraemax)
    for eadded in range(1, 51):
        extraedgesnum.append(eadded)
        etoadd = random.choice(extraeset)
        extraeset.remove(etoadd)
        Grafsiec.add_edges_from([etoadd])
        Grafsiec[etoadd[0]][etoadd[1]]["capacity"] = avgcap
        wyniki.append(reliabilitystat(Grafsiec, macNat, 0.05, 0.02, tests=500, maxeload=1.0))
    plt.plot(extraedgesnum, wyniki)
    plt.axis([1,50, 0, 1])
    plt.show()
    print(wyniki)
    print(extraedgesnum)

zadc()
        
        
        
        
