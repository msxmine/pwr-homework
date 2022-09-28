import matplotlib.pyplot as plt

plt.grid(True, "both", "both", color=(0.0,1.0,0.0), linewidth=0.1)
plt.xlim((0,10))
plt.ylim((0,15))
plt.xticks(range(1,10))
plt.yticks(range(1,15))
plt.gca().set_aspect("equal")
plt.gca().tick_params(color=(0.0,1.0,0.0), labelcolor=(0.0,1.0,0.0))
for spine in plt.gca().spines.values():
    spine.set_edgecolor((0.0,1.0,0.0))
plt.savefig("gridpaper.png", dpi=1200, bbox_inches="tight")
#plt.show()
