import sys
import matplotlib.pyplot as plt
Ef = float(sys.argv[1])
pathlist = sys.argv[2:]
kpath = "band.in";
kLabels = [];
kLGaps = [];
kLNum = 0
with open(kpath, "r") as f:
    line = f.readline()
    while(line.strip() != "K_POINTS {crystal_b}" and line):
        line = f.readline()
    kLNum = int(f.readline())
    line = f.readline()
    while(len(line) > 1):
        L_G = line.split()
        kLabels.append(L_G[0])
        kLGaps.append(int(L_G[1]))
        line = f.readline()
fmstr = ['b--', 'r-']
ind = 0
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for path in pathlist:
    with open(path, "r") as bFile:
        kpoints = []
        Es = []
        for inLine in bFile:
            k_E = inLine.split()
            if len(k_E):
                kpoints.append(float(k_E[0]))
                Es.append(float(k_E[1]) - Ef)
    plt.scatter(kpoints, Es, s=2)
    fmind = 1
kLIndex = []
for i in range(kLNum):
    kLIndex.append(kpoints[sum(kLGaps[:i])])
plt.xlabel("k")
plt.ylabel("E-Ef (eV)")
plt.xticks(kLIndex)
ax.set_xticklabels(kLabels)
plt.legend(pathlist)
plt.grid(True)
plt.xlim(min(kpoints), max(kpoints))
plt.ylim(-5, 5)
plt.show()