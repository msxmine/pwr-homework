import matplotlib.pyplot as plt

xaxis = []
nolu = []
withlu = []

datafil = open("testseries2.txt", "r")
lines =  datafil.readlines()
lines = [x.split(" ") for x in lines]
datafil.close()

for i in range(0, len(lines), 4):
    xaxis.append(lines[i][0])
    nolu.append({
        "noswap": {
            "memory": int(lines[i][3]),
            "time": float(lines[i][4])
        },
        "swap": {
            "memory": int(lines[i+1][3]),
            "time": float(lines[i+1][4])
        }
    })
    withlu.append({
        "noswap": {
            "memory": int(lines[i+2][3]),
            "timelu": float(lines[i+2][4]),
            "time": float(lines[i+2][5])
        },
        "swap": {
            "memory": int(lines[i+3][3]),
            "timelu": float(lines[i+3][4]),
            "time": float(lines[i+3][5])
        }
    })

fig, axs = plt.subplots(2)

axs[0].plot(xaxis, [x["noswap"]["memory"] for x in nolu])
axs[0].plot(xaxis, [x["noswap"]["memory"] for x in withlu])
axs[0].legend(["NoLU", "LU"])
axs[0].set_title("alokacje RAM")

axs[1].plot(xaxis, [x["noswap"]["time"] for x in nolu])
axs[1].plot(xaxis, [x["swap"]["time"] for x in nolu])

axs[1].plot(xaxis, [x["noswap"]["time"] + x["noswap"]["timelu"] for x in withlu])
axs[1].plot(xaxis, [x["swap"]["time"] + x["swap"]["timelu"] for x in withlu])

axs[1].plot(xaxis, [x["noswap"]["time"] for x in withlu])
axs[1].plot(xaxis, [x["swap"]["time"] for x in withlu])

axs[1].legend(["NoLU-NoSwap", "NoLU-Swap", "LU-NoSwap", "LU-Swap", "LUSolve-NoSwap", "LUSolve-Swap"])
axs[1].set_title("czas obliczeń")

plt.show()
