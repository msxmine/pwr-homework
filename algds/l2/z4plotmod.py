#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import statistics

dostepnetyp = ["int","str"]
cont = {}

for k in dostepnetyp:
    data = {}

    plik = open("z4k10" + str(k) + ".txt", "r")

    for raw in plik.readlines():
        line = raw.rstrip().split()
        if line[4] not in data:
            data[line[4]] = {}
        if int(line[0]) not in data[line[4]]:
            data[line[4]][int(line[0])] = [[],[],[]]
        data[line[4]][int(line[0])][0].append(int(line[1]))
        data[line[4]][int(line[0])][1].append(int(line[2]))
        data[line[4]][int(line[0])][2].append(float(line[3]))
    for algo in data:
        for siz in data[algo]:
            data[algo][siz][0] = statistics.fmean(data[algo][siz][0])
            data[algo][siz][1] = statistics.fmean(data[algo][siz][1])
            data[algo][siz][2] = statistics.fmean(data[algo][siz][2])
            
    cont[k] = data


fig, axs = plt.subplots(len(cont),5)

for idx, k in enumerate(cont):
    for algo in cont[k]:
#        if algo != "insertionsort":
            x = [*(cont[k][algo])]
            y1 = [ cont[k][algo][n][0] for n in x]
            y2 = [ cont[k][algo][n][1] for n in x]
            y3 = [ cont[k][algo][n][2] for n in x]
            y4 = [ (cont[k][algo][n][0])/n for n in x]
            y5 = [ (cont[k][algo][n][1])/n for n in x]
            
            axs[idx,0].plot(x,y1, label=algo)
            axs[idx,1].plot(x,y2, label=algo)
            axs[idx,2].plot(x,y3, label=algo)
            axs[idx,3].plot(x,y4, label=algo)
            axs[idx,4].plot(x,y5, label=algo)
            
    axs[idx,0].legend(loc="upper left")
    axs[idx,1].legend(loc="upper left")
    axs[idx,2].legend(loc="upper left")
    axs[idx,3].legend(loc="upper left")
    axs[idx,4].legend(loc="upper left")
    
    axs[idx,0].set_ylabel("TYP="+str(k), size="large")
    
axs[0,0].set_title("Porównania")
axs[0,1].set_title("Przestawienia")
axs[0,2].set_title("Czas")
axs[0,3].set_title("Porównania/N")
axs[0,4].set_title("Przestawienia/N")

plt.show()
