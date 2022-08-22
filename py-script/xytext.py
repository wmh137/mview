import sys
import matplotlib.pyplot as plt
labelType = sys.argv[1]
skipLine = int(sys.argv[2])
pathNum = len(sys.argv)
for i in range(3, pathNum):
    path = sys.argv[i]
    rFile = open(path, "r")
    X = []
    Y = []
    inXY = ["", ""]
    for j in range(skipLine):
        rFile.readline()
    inLine = rFile.readline()
    while(inLine):
        inXY = inLine.split()
        X.append(float(inXY[0]))
        Y.append(float(inXY[1]))
        inLine = rFile.readline()
    rFile.close()
    plt.plot(X, Y, label = path)
if(labelType == "raman"):
    plt.xlabel("Raman Shift (cm$^{-1}$)")
    plt.ylabel("Intensity (a.u.)")
elif(labelType == "xrd"):
    plt.xlabel("$\\theta\\ (\degree)$")
    plt.ylabel("Intensity (a.u.)")
elif(labelType == "xy"):
    plt.xlabel("x")
    plt.ylabel("y")
plt.title(labelType)
plt.legend()
plt.show()
