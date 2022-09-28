#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import statistics

knames = ["k=30", "k=n/2", "k=n-30"]
alcolors = ["blue", "orange", "cyan", "gold"]
data = {}

plik = open("z1out.txt", "r")

for raw in plik.readlines():
    line = raw.rstrip().split()
    dataset = line[0]
    algo = line[1]
    n = int(line[2])
    k = int(line[3])
    comp = int(line[5])
    swap = int(line[6])
    
    if k not in data:
        data[k] = {}
    if dataset not in data[k]:
        data[k][dataset] = {}
    if algo not in data[k][dataset]:
        data[k][dataset][algo] = {}
    if n not in data[k][dataset][algo]:
        data[k][dataset][algo][n] = [[],[]]

    data[k][dataset][algo][n][0].append(comp)
    data[k][dataset][algo][n][1].append(swap)

for k in data:
    for dataset in data[k]:
        for algo in data[k][dataset]:
            for n in data[k][dataset][algo]:
                data[k][dataset][algo][n].append(statistics.fmean(data[k][dataset][algo][n][0]))
                data[k][dataset][algo][n].append(statistics.fmean(data[k][dataset][algo][n][1]))
                data[k][dataset][algo][n].append(statistics.stdev(data[k][dataset][algo][n][0]))
                data[k][dataset][algo][n].append(statistics.stdev(data[k][dataset][algo][n][1]))


fig, axs = plt.subplots(3,4)

for idx, k in enumerate(data):
    for dsi, dataset in enumerate(data[k]):
        for alidx, algo in enumerate(data[k][dataset]):
            x = [*(data[k][dataset][algo])]
            y1 = [ data[k][dataset][algo][n][2] for n in x]
            y2 = [ data[k][dataset][algo][n][3] for n in x]
            y1dev = [ data[k][dataset][algo][n][4] for n in x]
            y2dev = [ data[k][dataset][algo][n][5] for n in x]
            
            for n in data[k][dataset][algo]:
                axs[idx,0+(dsi*2)].scatter([n]*len(data[k][dataset][algo][n][0]), data[k][dataset][algo][n][0], marker="o", s=(1.)**2, c=alcolors[alidx+2])
                axs[idx,1+(dsi*2)].scatter([n]*len(data[k][dataset][algo][n][1]), data[k][dataset][algo][n][1], marker="o", s=(1.)**2, c=alcolors[alidx+2])
            axs[idx,0+(dsi*2)].errorbar(x,y1, yerr=y1dev ,label=algo)
            axs[idx,1+(dsi*2)].errorbar(x,y2, yerr=y2dev, label=algo)
            
        axs[idx,0+(dsi*2)].legend(loc="upper left")
        axs[idx,1+(dsi*2)].legend(loc="upper left")
    
    axs[idx,0].set_ylabel(knames[k], size="large")
    
axs[0,0].set_title("Losowe dane, Porównania")
axs[0,1].set_title("Losowe dane, Przestawienia")
axs[0,2].set_title("Permutacja, Porównania")
axs[0,3].set_title("Permutacja, Przestawienia")

plt.show()
