import matplotlib.pyplot as plt
import json

with open("./times.json", "r") as tfil:
    tjs = json.load(tfil)

xaxis = [int(x) for x in tjs]
y1 = [float(tjs[x]["cls"]) for x in tjs]
y2 = [float(tjs[x]["crt"]) for x in tjs]

y1d = [float(tjs[x]["cls"])/(int(x)**2) for x in tjs]
y2d = [float(tjs[x]["crt"])/(int(x)**2) for x in tjs]

fig, ax = plt.subplots(1,2)

ax[0].plot(xaxis, y1, label="Klasyczny")
ax[0].plot(xaxis, y2, label="CRT")
ax[0].legend()
ax[0].set(ylabel="Czas", xlabel="Wielkość liczb pierwszych")

ax[1].plot(xaxis, y1d, label="Klasyczny")
ax[1].plot(xaxis, y2d, label="CRT")
ax[1].legend()
ax[1].set(ylabel="Czas/x^2", xlabel="Wielkość liczb pierwszych")
plt.show()
