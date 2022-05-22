''' phband.py *.gp [matdyn.in]'''
import sys
import numpy as np
import matplotlib.pyplot as plt
path = sys.argv[1]
qpath = "matdyn.in";
if(len(sys.argv) > 2):
    qpath = sys.argv[2]
qLabels = [];
qLGaps = [];
qLNum = 0
with open(qpath, "r") as f:
    line = f.readline()
    while(line.strip() != "/" and line):
        line = f.readline()
    qLNum = int(f.readline())
    line = f.readline()
    while(line):
        L_G = line.split()
        qLabels.append(L_G[0])
        qLGaps.append(int(L_G[1]))
        line = f.readline()
qBand = []
with open(path, "r") as f:
    for line in f:
        qBand.append(list(map(float, line.split())))
    qBandnp = np.array(qBand)
qLIndex = []
for i in range(qLNum):
    qLIndex.append(qBandnp[sum(qLGaps[:i]), 0])
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for i in range(1, qBandnp.shape[1]):
    plt.plot(qBandnp[:, 0], qBandnp[:, i])
plt.xticks(qLIndex)
ax.set_xticklabels(qLabels)
plt.grid(True)
plt.xlim(min(qBandnp[:, 0]), max(qBandnp[:, 0]))
plt.ylabel("Frequency(cm$^{-1}$)")
plt.show()