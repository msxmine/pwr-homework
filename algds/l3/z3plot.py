#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import statistics
import math

knames = ["v~=0", "v~=n/2", "v~=n", "v=rand not found", "v=rand"]

data = {}

plik = open("z3out.txt", "r")

for raw in plik.readlines():
    line = raw.rstrip().split()
    val = knames[int(line[0])]
    n = int(line[1])
    tests = int(line[2])
    comp = int(line[3])
    exect = int(line[4])
    
    if val not in data:
        data[val] = {}
    if n not in data[val]:
        data[val][n] = []

    data[val][n].append(comp/tests)
    data[val][n].append(exect/tests)


fig, axs = plt.subplots(2,3)

for val in data:
    x = [*(data[val])]
    y1 = [ data[val][n][0] for n in x]
    y2 = [ data[val][n][1] for n in x]
    y3 = [ data[val][n][0]/math.log2(n) for n in x]
    y4 = [ data[val][n][1]/math.log2(n) for n in x]
    y5 = [ (data[val][n][0] / 5.0) - math.log2(n) for n in x]
    y6 = [ (data[val][n][1] / 5.0) - math.log2(n) for n in x]
            
    axs[0,0].plot(x,y1,label=val)
    axs[1,0].plot(x,y2,label=val)
    axs[0,1].plot(x,y3,label=val)
    axs[1,1].plot(x,y4,label=val)
    axs[0,2].plot(x,y5,label=val)
    axs[1,2].plot(x,y6,label=val)
        
axs[0,0].legend(loc="upper left")
axs[1,0].legend(loc="upper left")
axs[0,1].legend(loc="upper left")
axs[1,1].legend(loc="upper left")
axs[0,2].legend(loc="upper left")
axs[1,2].legend(loc="upper left")


axs[0,0].set_ylabel("Porównania", size="large")
axs[1,0].set_ylabel("Czas", size="large")
    
axs[0,0].set_title("Y")
axs[0,1].set_title("Y/log2(x)")
axs[0,2].set_title("Y/5.0 - log2(x)")

plt.show()
