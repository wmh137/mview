import sys
import matplotlib.pyplot as plt
Ef = float(sys.argv[1])
pathlist = sys.argv[2:]
fmstr = ['b--', 'r-']
ind = 0
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
    plt.xlabel("k")
    plt.ylabel("E (eV)")
    fmind = 1
plt.legend(pathlist)
plt.grid(True)
plt.ylim(-5, 5)
plt.show()