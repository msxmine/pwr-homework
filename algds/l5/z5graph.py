import matplotlib.pyplot as plt
import numpy as np
import statistics

data = {}

fig, axs = plt.subplots(1,5)

for idx, graphtype in enumerate(data[100]):
    x = [*(data)]
    y1 = [ data[n][graphtype]["dfs"]/n for n in x]
    y2 = [ data[n][graphtype]["rw"]/n for n in x]
    y3 = [ data[n][graphtype]["rr"]/n for n in x]

    axs[idx].plot(x,y1, label="dfs/n")
    axs[idx].plot(x,y2, label="rw/n")
    axs[idx].plot(x,y3, label="rr/n")

    axs[idx].legend(loc="upper left")
    axs[idx].set_title(graphtype)

plt.show()
