#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import statistics

data = {}

plik = open("z1result.txt", "r")

for raw in plik.readlines():
    line = raw.rstrip().split()
    size = int(line[0])
    tinsert = int(line[1])
    tdelete = int(line[2])

    if size not in data:
        data[size] = []

    data[size].append(tinsert/1000)
    data[size].append(tdelete/1000)



fig, axs = plt.subplots(1,2)


x = [*(data)]
y1 = [ data[n][0] for n in x]
y2 = [ data[n][1] for n in x]
axs[0].plot(x,y1, label="pqueue")
axs[1].plot(x,y2, label="pqueue")


            
axs[0].legend(loc="upper left")
axs[1].legend(loc="upper left")

    
axs[0].set_title("Insert")
axs[1].set_title("Delete")


plt.show()
